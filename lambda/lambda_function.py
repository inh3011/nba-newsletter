import os
import boto3
import smtplib
from email.message import EmailMessage
from nba_api.live.nba.endpoints import scoreboard
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("USERS_TABLE_NAME", "Users"))

# 📄 템플릿 설정
env = Environment(loader=FileSystemLoader("."))  # 현재 디렉토리에서 로딩
template = env.get_template("newsletter_template.html")

def send_email(to_email, subject, html_body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("GMAIL_ADDRESS")
    msg["To"] = to_email
    msg.set_content("HTML을 지원하지 않는 경우를 위한 텍스트 메일입니다.")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("GMAIL_ADDRESS"), os.getenv("GMAIL_APP_PASSWORD"))
        server.send_message(msg)

def lambda_handler(event, context):
    games = scoreboard.ScoreBoard().get_dict()["scoreboard"]["games"]
    today = datetime.now().strftime("%Y-%m-%d")

    today_teams = set()
    for game in games:
        today_teams.add(game["homeTeam"]["teamTricode"])
        today_teams.add(game["awayTeam"]["teamTricode"])

    # 유저 조회
    users = table.scan().get("Items", [])

    for user in users:
        email = user.get("email")
        teams = user.get("teams", [])  # [{ "abbreviation": "GSW", ... }]

        fav_abbr = [t["abbreviation"] for t in teams]
        matched_games = [
            game for game in games
            if game["homeTeam"]["teamTricode"] in fav_abbr or game["awayTeam"]["teamTricode"] in fav_abbr
        ]

        if matched_games:
            html_body = template.render(date=today, games=matched_games)
            send_email(email, f"{today} NBA 뉴스레터", html_body)

    return {"statusCode": 200, "body": "Emails sent"}