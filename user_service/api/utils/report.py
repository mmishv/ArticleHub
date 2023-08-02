import pika
import json
from datetime import datetime, timedelta
from user_service.api.utils.crud import get_users

def send_article_count_notifications():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='article_count_notifications')

    users = get_users()  # Получаем всех пользователей из базы данных

    for user in users:
        article_count = count_published_articles_last_5_minutes()  # Используем функцию из article_service
        message = {
            "email": user.email,
            "article_count": article_count,
        }
        channel.basic_publish(exchange='', routing_key='article_count_notifications', body=json.dumps(message))

    connection.close()

def listen_to_article_count_notifications():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='article_count_notifications')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        email = message['email']
        article_count = message["article_count"]

        with open("article_count_notifications.txt", "a") as file:
            file.write(f"User {email} published {article_count} articles in the last 5 minutes.\n")

    channel.basic_consume(queue='article_count_notifications', on_message_callback=callback, auto_ack=True)
    print("Listening for article count notifications...")
    channel.start_consuming()
