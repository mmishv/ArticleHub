import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httpx

from article_service.api.utils.article_utils import count_published_articles
from common.settings import HOST, PORT


def send_daily_report():
    smtp_server = "server"
    smtp_port = 587
    smtp_username = "username"
    smtp_password = "password"
    sender_email = "sender@gmail.com"

    users_response = httpx.get(f"http://{HOST}:{PORT}/users/")
    users_data = users_response.json()

    for user in users_data:
        receiver_email = user["email"]

        published_articles_count = count_published_articles()

        report_text = f"Daily Report for {user['first_name']} {user['last_name']}\n\n"
        report_text += f"Number of published articles in the last 24 hours: {published_articles_count}\n"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Daily Report: Number of Published Articles"

        body = MIMEText(report_text, 'plain')
        msg.attach(body)

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Daily report sent successfully to {receiver_email}")
        except Exception as e:
            print(f"Failed to send daily report to {receiver_email}: {e}")
