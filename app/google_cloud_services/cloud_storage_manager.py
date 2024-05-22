from datetime import timedelta
from google.cloud import storage

from config.global_constants import CREDENTIALS_INFO_CLOUD_STORAGE


class GoogleCloudStorageManager:
    def __init__(self, bucket_name, credentials_file):
        self.bucket_name = bucket_name
        credentials_file = credentials_file
        self.storage_client = storage.Client.from_service_account_info(
            CREDENTIALS_INFO_CLOUD_STORAGE
        )

    def upload_file(self, local_file, destination_blob_name):
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(local_file)
        return blob.public_url

    def upload_file_by_file_name(self, local_file_name, destination_blob_name):
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_name)
        return blob.public_url

    def download_file(self, blob_name, destination_local_path):
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(destination_local_path)

    def generate_signed_url(self, blob_name, expiration=3600):
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        expiration_time = timedelta(seconds=expiration)
        url = blob.generate_signed_url(expiration=expiration_time, method="GET")
        return url
