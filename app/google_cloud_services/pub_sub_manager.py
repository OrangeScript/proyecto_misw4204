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
            except TimeoutError as e:
                print(f"\nTimeout error while subscribing: {str(e)}")
                self.streaming_pull_future.cancel()
                self.streaming_pull_future.result()
            except Exception as e:
                print(f"\nError occurred while subscribing: {str(e)}")
