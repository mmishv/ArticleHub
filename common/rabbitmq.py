

import pika
from pydantic import json

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))

channel = connection.channel()
channel.queue_declare(queue="email_queue")

RABBITMQ_ARTICLE_QUEUE = "article_notifications"


def publish_article_notification(article_id: str):
    channel.queue_declare(queue=RABBITMQ_ARTICLE_QUEUE)

    message = {"article_id": article_id}
    channel.basic_publish(exchange="", routing_key=RABBITMQ_ARTICLE_QUEUE, body=json.dumps(message))

    print(f"Published article notification for article ID: {article_id}")


def handle_article_notification(ch, method, properties, body):
    article_data = json.loads(body)
    article_id = article_data.get("article_id")
    if article_id:
        print(f"Received article notification for article ID: {article_id}")
        publish_article_notification(article_id)


channel.basic_consume(queue=RABBITMQ_ARTICLE_QUEUE, on_message_callback=handle_article_notification, auto_ack=True)
print("Waiting for article notifications. To exit press CTRL+C")
channel.start_consuming()
