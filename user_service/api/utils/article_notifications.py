import json

import pika

from user_service.api.utils.crud import get_user_by_email, get_all_users


def callback(ch, method, properties, body):
    message = json.loads(body)
    email = message['author']
    article_title = message["article_title"]

    user_info = get_user_by_email(email)

    if user_info:
        with open("notifications.txt", "a") as file:
            for user in get_all_users():
                file.write(
                    f"Hello {user.first_name} {user.last_name}!"
                    f" User {user_info.email} added an article: {article_title}\n")


def listen_to_article_notifications():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='article_notifications')
    channel.basic_consume(queue='article_notifications', on_message_callback=callback, auto_ack=True)
    print("Listening for article notifications...")
    channel.start_consuming()
