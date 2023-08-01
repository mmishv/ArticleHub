import pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))

channel = connection.channel()
