import boto3
import os
import json
from nba_api.live.nba.endpoints import scoreboard
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# --- AWS Resource Setup ---
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("users")
sqs = boto3.client("sqs")
SQS_URL = os.getenv("SQS_QUEUE_URL")

# --- Jinja2 Template Setup ---
env = Environment(loader=FileSystemLoader(".."))
template = env.get_template("newsletter_template.html")

def get_today_games():
    """
    Fetch today's NBA games using nba_api.

    Returns:
        list: A list of game dictionaries for today.
    """
    return scoreboard.ScoreBoard().get_dict()["scoreboard"]["games"]

def get_user_matched_games(user_teams, games):
    """
    Filter games where the user's favorite teams are playing.

    Args:
        user_teams (list): List of teams the user follows.
        games (list): List of all games for the day.

    Returns:
        list: A list of games where the user's teams are playing.
    """
    abbreviations = [team["abbreviation"] for team in user_teams]
    return [
        game for game in games
        if game["homeTeam"]["teamTricode"] in abbreviations or
           game["awayTeam"]["teamTricode"] in abbreviations
    ]

def create_newsletter_html(date_str, games):
    """
    Render HTML for the newsletter using the Jinja2 template.

    Args:
        date_str (str): The current date string.
        games (list): A list of filtered games.

    Returns:
        str: Rendered HTML string.
    """
    return template.render(date=date_str, games=games)

def send_to_sqs(email, subject, html_body):
    """
    Send the rendered newsletter HTML as a message to an SQS queue.

    Args:
        email (str): Recipient's email address.
        subject (str): Email subject.
        html_body (str): HTML content of the email.
    """
    sqs.send_message(
        QueueUrl=SQS_URL,
        MessageBody=json.dumps({
            "email": email,
            "subject": subject,
            "html_body": html_body
        })
    )


def lambda_handler(event, context):
    """
    AWS Lambda handler to generate newsletters and send messages to SQS
    for users whose favorite teams have games today.

    Args:
        event (dict): AWS Lambda event payload.
        context (LambdaContext): AWS Lambda context object.

    Returns:
        dict: Result status with a message.
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    games = get_today_games()
    users = table.scan().get("Items", [])

    for user in users:
        email = user.get("email")
        teams = user.get("teams", [])

        matched_games = get_user_matched_games(teams, games)
        if not matched_games:
            continue

        html = create_newsletter_html(today_str, matched_games)
        send_to_sqs(email, f"NBA Newsletter - {today_str}", html)

    return {"statusCode": 200, "message": "Messages pushed to SQS"}