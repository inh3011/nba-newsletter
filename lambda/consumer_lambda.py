import json
import os
import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, html_body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("GMAIL_ADDRESS")
    msg["To"] = to_email
    msg.set_content("Your email client does not support HTML.")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("GMAIL_ADDRESS"), os.getenv("GMAIL_APP_PASSWORD"))
        server.send_message(msg)

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        send_email(body["email"], body["subject"], body["html_body"])

    return {"statusCode": 200, "message": "Emails sent"}