import boto3
import os
import json
from nba_api.live.nba.endpoints import scoreboard
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("USERS_TABLE_NAME", "Users"))

sqs = boto3.client("sqs")
SQS_URL = os.getenv("SQS_QUEUE_URL")

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("newsletter_template.html")

def lambda_handler(event, context):
    today = datetime.now().strftime("%Y-%m-%d")
    games = scoreboard.ScoreBoard().get_dict()["scoreboard"]["games"]
    today_teams = {g["homeTeam"]["teamTricode"] for g in games} | \
                  {g["awayTeam"]["teamTricode"] for g in games}

    users = table.scan().get("Items", [])
    for user in users:
        email = user["email"]
        teams = user.get("teams", [])
        abbreviations = [t["abbreviation"] for t in teams]

        matched_games = [
            g for g in games
            if g["homeTeam"]["teamTricode"] in abbreviations or
               g["awayTeam"]["teamTricode"] in abbreviations
        ]

        if not matched_games:
            continue

        html_body = template.render(
            date=today,
            games=matched_games
        )

        sqs.send_message(
            QueueUrl=SQS_URL,
            MessageBody=json.dumps({
                "email": email,
                "subject": f"NBA Newsletter - {today}",
                "html_body": html_body
            })
        )

    return {"statusCode": 200, "message": "Messages pushed to SQS"}