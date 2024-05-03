import json
from config.global_constants import (
    RABBITMQ_SERVER_HOST,
    RABBITMQ_QUEUE_NAME,
)
from video_processor_worker.rabbitMqConfig import RabbitMQ


def send_message_to_RabbitMQ(message):
    rabbitmq = RabbitMQ(RABBITMQ_SERVER_HOST, RABBITMQ_QUEUE_NAME)
    rabbitmq.connect()
    rabbitmq.send_message(json.dumps(message))
    rabbitmq.close_connection()
