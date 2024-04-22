import pika
import threading
from config.global_constants import (
    RABBIT_ADMIN_PASSWORD,
    RABBIT_ADMIN_USER,
)


class RabbitMQ:
    def __init__(self, host, queue_name):
        self.host = host
        self.queue_name = queue_name
        self.messages = []
        self.connection = None
        self.channel = None
        self.consume_thread = threading.Thread(target=self.consume_messages)
        self.consume_thread.daemon = True

    def connect(self):
        try:
            if self.connection is None or self.channel is None:
                credentials = pika.PlainCredentials(
                    RABBIT_ADMIN_USER, RABBIT_ADMIN_PASSWORD
                )

                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, credentials=credentials)
                )
                self.channel = self.connection.channel()
                print(f"\nSuccessful connection RabbitMQ in Host: [ {self.host} ]")

            self.channel.queue_declare(queue=self.queue_name, durable=False)
            print(f"\nQueue [ {self.queue_name} ] declared successfully.")
        except pika.exceptions.AMQPError as e:
            print("\nError:", e)

    def send_message(self, message, queue_name):
        try:
            self.channel.basic_publish(
                exchange="", routing_key=queue_name, body=message
            )
            print("\n[x] Sent: %r" % message)
        except pika.exceptions.AMQPError as e:
            print("\nError sending message:", e)

    def consume_messages(self, process_message_func):
        while True:
            try:
                for method_frame, properties, body in self.channel.consume(
                    self.queue_name, inactivity_timeout=1
                ):
                    if body is None:
                        break
                    process_message_func(body)
                    self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            except pika.exceptions.AMQPError as e:
                print("\nError when consuming message:", e)

    def start_consuming(self, process_message_func):
        if self.connection is None or self.channel is None:
            self.connect()
        self.consume_thread = threading.Thread(
            target=self.consume_messages, args=(process_message_func,)
        )
        self.consume_thread.daemon = True
        self.consume_thread.start()
        print("\nConsuming messages...")

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            print("\nConnection closed.\n")
