from google_cloud_services.pub_sub_manager import PubSubManager
from google_cloud_services.cloud_storage_manager import GoogleCloudStorageManager
from config.global_constants import (
    GOOGLE_CLOUD_PUB_SUB_CREDENTIALS,
    GOOGLE_CLOUD_PUB_SUB_TOPIC_PATH,
    GOOGLE_CLOUD_STORAGE_BUCKET,
    GOOGLE_CLOUD_STORAGE_CREDENTIALS,
)


def publish_message_to_pub_sub(task):
    try:
        task_id = task["task_id"]
        pubsub_manager = PubSubManager(GOOGLE_CLOUD_PUB_SUB_CREDENTIALS)
        topic_path = GOOGLE_CLOUD_PUB_SUB_TOPIC_PATH
        data = f"Processing task: {task_id}"
        message_published_id = pubsub_manager.publish_message(topic_path, data, **task)
        print(
            f"Message published in {GOOGLE_CLOUD_PUB_SUB_TOPIC_PATH} topic with id: {message_published_id}"
        )
        return message_published_id
    except Exception as e:
        raise Exception(f"Error publishing message: {str(e)}")


def upload_video_to_google_cloud_storage(file, filename):
    try:
        storage_manager = GoogleCloudStorageManager(
            GOOGLE_CLOUD_STORAGE_BUCKET, GOOGLE_CLOUD_STORAGE_CREDENTIALS
        )

        storage_manager.upload_file(file, filename)
        print(
            f"File {filename} uploaded successfully to: {GOOGLE_CLOUD_STORAGE_BUCKET} bucket"
        )
    except Exception as e:
        raise Exception(
            f"Failed to upload {filename} to {GOOGLE_CLOUD_STORAGE_BUCKET} bucket, error: {str(e)}"
        )


def generate_google_cloud_storage_signed_url(item_bucket_name):
    try:
        storage_manager = GoogleCloudStorageManager(
            GOOGLE_CLOUD_STORAGE_BUCKET, GOOGLE_CLOUD_STORAGE_CREDENTIALS
        )
        signed_url = storage_manager.generate_signed_url(item_bucket_name)
        return signed_url
    except Exception as e:
        raise Exception(f"Error creating signed url: {str(e)}")
