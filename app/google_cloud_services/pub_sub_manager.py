from google.cloud import pubsub_v1


class PubSubManager:
    def __init__(self, credentials_path):
        self.publisher = pubsub_v1.PublisherClient.from_service_account_file(
            credentials_path
        )
        self.subscriber = pubsub_v1.SubscriberClient.from_service_account_file(
            credentials_path
        )

    def publish_message(self, topic_path, data, **attributes):
        data = data.encode("utf-8")
        future = self.publisher.publish(topic_path, data, **attributes)
        return future.result()

    def subscribe_to_topic(self, subscription_path, callback):
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path, callback=callback
        )
        return streaming_pull_future.result()

    def listen_for_messages(self, subscription_path, callback):
        with self.subscriber:
            try:
                self.subscribe_to_topic(subscription_path, callback)
            except TimeoutError:
                self.streaming_pull_future.cancel()
                self.streaming_pull_future.result()


""" # Uso de la clase PubSubManager
credentials_path = "/Users/ccxc/Desktop/U/MISW4204/proyecto_misw4204/app/google_cloud_services/GOOGLE_CLOUD_PUB_SUB_CREDENTIALS.json"
pubsub_manager = PubSubManager(credentials_path)

topic_path = "projects/misw4204-recover/topics/video_processing_tasks"
data = "New message"
task = {"id": "1", "task_id": "1", "video_id": "1"}

print(
    f"Mensaje publicado, id: {pubsub_manager.publish_message(topic_path, data, **task)}"
)

subscription_path = "projects/misw4204-recover/subscriptions/video_processing_tasks-sub"


def callback(message):
    print(f"Mensaje recibido: {message}")
    if message.attributes:
        print("Propiedades:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")
    message.ack()


pubsub_manager.listen_for_messages(subscription_path, callback)
 """
