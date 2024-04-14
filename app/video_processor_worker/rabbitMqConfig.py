import pika
import threading


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
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
        except pika.exceptions.AMQPError as e:
            print("\nConnection error:", e)

    def ensure_queue_exists(self):
        if self.connection is None or self.channel is None:
            self.connect()

        try:
            self.channel.queue_declare(queue=self.queue_name, durable=False)
            print(
                f"\nQueue declared successfully, Host: [ {self.host} ], Queue: [ {self.queue_name} ]"
            )
        except pika.exceptions.AMQPError as e:
            print("\nError declaring queue:", e)

    def send_message(self, message, queue_name):
        try:
            self.channel.basic_publish(
                exchange="", routing_key=queue_name, body=message
            )
            print(" [x] Sent %r" % message)
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
                print(e)

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
            print("\nConnection closed.")
