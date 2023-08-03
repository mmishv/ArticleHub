import time
from datetime import datetime

import pika
import requests
from celery import Celery

app = Celery('api.celery_app')


@app.task(name='api.celery_app.send_article_count_notifications')
def send_article_count_notifications():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='article_count_notifications')

    response = requests.get(f"http://localhost:8001/article_count_last_5_minutes")
    article_count = response.json()["article_count"]

    message = f"{datetime.now()}: {article_count} articles published in the last 5 minutes\n"

    with open("article_count_notifications.txt", "a") as file:
        file.write(message)

    time.sleep(60)
