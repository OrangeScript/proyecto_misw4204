from google.cloud import pubsub_v1
from concurrent.futures import ThreadPoolExecutor
from google.cloud.pubsub_v1.subscriber.scheduler import ThreadScheduler
from google.cloud.pubsub_v1.types import FlowControl

from config.global_constants import CREDENTIALS_INFO_PUB_SUB


class PubSubManager:
    def __init__(self, credentials_path):
        self.publisher = pubsub_v1.PublisherClient.from_service_account_info(
            CREDENTIALS_INFO_PUB_SUB
        )
        self.subscriber = pubsub_v1.SubscriberClient.from_service_account_info(
            CREDENTIALS_INFO_PUB_SUB
        )

    def publish_message(self, topic_path, data, **attributes):
        data = data.encode("utf-8")
        future = self.publisher.publish(topic_path, data, **attributes)
        return future.result()

    def subscribe_to_topic(self, subscription_path, callback):
        flow_control = FlowControl(max_messages=1)
        executor = ThreadPoolExecutor(max_workers=1)
        scheduler = ThreadScheduler(executor)

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback,
            scheduler=scheduler,
            flow_control=flow_control,
        )
        streaming_pull_future.result()

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
