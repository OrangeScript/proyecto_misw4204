from ftplib import FTP
import json
import os
from config.global_constants import (
    ASSETS_PATH,
    FTP_ADMIN_USER,
    FTP_PASSWORD,
    FTP_REMOTE_SERVER,
    FTP_VIDEOS_FOLDER,
    RABBITMQ_SERVER_HOST,
    RABBITMQ_QUEUE_NAME,
    VIDEO_FOLDER_NAME,
)
from video_processor_worker.rabbitMqConfig import RabbitMQ


def upload_file_ftp(file, remote_name):
    with FTP(FTP_REMOTE_SERVER) as ftp:
        ftp.login(FTP_ADMIN_USER, FTP_PASSWORD)
        """ if FTP_VIDEOS_FOLDER not in ftp.nlst():
            ftp.mkd(FTP_VIDEOS_FOLDER) """
        """ ftp.cwd(FTP_VIDEOS_FOLDER) """

        ftp.storbinary(f"STOR {remote_name}", file.stream)

        print(
            f"\nFile {remote_name} uploaded successfully to {FTP_VIDEOS_FOLDER}/{remote_name}"
        )
        """ print(f"\nFile {remote_name} uploaded successfully to ftp/{remote_name}") """


def download_video_from_ftp_server(remote_file_name):
    try:
        ftp = FTP(FTP_REMOTE_SERVER)
        ftp.login(user=FTP_ADMIN_USER, passwd=FTP_PASSWORD)
        """ ftp.cwd(FTP_VIDEOS_FOLDER) """
        local_path = f"{ASSETS_PATH}/{VIDEO_FOLDER_NAME}/{remote_file_name}"
        with open(local_path, "wb") as file:
            ftp.retrbinary(f"RETR {remote_file_name}", file.write)
        ftp.quit()
        return f"File {remote_file_name} downloaded successfully to: {local_path}"
    except Exception as e:
        raise Exception(
            f"Failed to download {remote_file_name} from {FTP_VIDEOS_FOLDER}, error: {str(e)}"
        )


def send_message_to_RabbitMQ(message):
    rabbitmq = RabbitMQ(RABBITMQ_SERVER_HOST, RABBITMQ_QUEUE_NAME)
    rabbitmq.connect()
    rabbitmq.send_message(json.dumps(message), RABBITMQ_QUEUE_NAME)
    rabbitmq.close_connection()
