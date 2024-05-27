from datetime import datetime
import os
import json
import subprocess
from models.models import Worker_logs
from google_cloud_services.pub_sub_manager import PubSubManager
from google_cloud_services.cloud_storage_manager import GoogleCloudStorageManager
from config.global_constants import (
    ASSETS_PATH,
    GOOGLE_CLOUD_PUB_SUB_TOPIC_ERROR_PATH,
    GOOGLE_CLOUD_STORAGE_BUCKET,
    LOGO_NAME,
    LOGO_FOLDER_NAME,
    LOGO_VIDEO_ITEM_NAME,
    GLOBAL_VIDEO_SIZE,
    VIDEO_FOLDER_NAME,
)


def check_file_existence(file_path):
    try:
        if os.path.exists(file_path):
            return True
        else:
            return False
    except Exception as e:
        raise RuntimeError(f"Error checking file existence: {e}")


def remove_file(file_path):
    if check_file_existence(file_path):
        try:
            os.remove(file_path)
            return f"Removed: {file_path}"
        except Exception as e:
            raise Exception(f"Error removing file {file_path}: {e}")
    else:
        return f"File {file_path} does not exist."


def get_asset_path(type, name):
    try:
        project_path = "assets/"
        return f"{project_path}{type}/{name}"
    except Exception as e:
        raise RuntimeError(f"Error getting asset path: {e}")


def add_process_logs(logs, session, task_id, user_id, execution_time):
    log_file_path = "logs.txt"
    try:
        if not check_file_existence(log_file_path):
            with open(log_file_path, "w") as file:
                pass

        with open(log_file_path, "a") as file:
            file.write("\n")
            for log in logs:
                file.write(log + "\n")
        combined_logs = "\n".join(logs)
        timestamp = datetime.now()

        new_log = Worker_logs(
            log_string=combined_logs,
            id_task=task_id,
            id_user=user_id,
            timestamp=timestamp,
            execution_time=execution_time,
        )
        session.add(new_log)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error adding logs to the database: {e}")
        error_log = Worker_logs(
            log_string=f"Error processing logs: {e}",
            id_task=task_id,
            id_user=user_id,
            timestamp=timestamp,
            execution_time=execution_time,
        )
        session.add(error_log)
        session.commit()


def create_error_log(error_type, error_message, timestamp_str):
    error_log = {
        "error_type": error_type,
        "message": error_message,
        "timestamp": timestamp_str,
    }
    return json.dumps(error_log)


def create_logo_video():
    output_logo_video_path = get_asset_path(LOGO_FOLDER_NAME, LOGO_VIDEO_ITEM_NAME)
    logo_path = get_asset_path(LOGO_FOLDER_NAME, LOGO_NAME)
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-framerate",
                "25",
                "-t",
                "0.3",
                "-i",
                logo_path,
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=44100:cl=stereo",
                "-vf",
                f"scale={GLOBAL_VIDEO_SIZE},setsar=1:1",
                "-shortest",
                output_logo_video_path,
            ]
        )
        return f"{LOGO_VIDEO_ITEM_NAME} created..."
    except Exception as e:
        raise RuntimeError(f"Error creating logo video: {e}")


def download_video_from_google_cloud_storage(remote_file_name):
    try:
        storage_manager = GoogleCloudStorageManager(GOOGLE_CLOUD_STORAGE_BUCKET)
        local_path = f"{ASSETS_PATH}/{VIDEO_FOLDER_NAME}/{remote_file_name}"
        storage_manager.download_file(remote_file_name, local_path)
        return f"File {GOOGLE_CLOUD_STORAGE_BUCKET}/{remote_file_name} downloaded successfully to: {local_path}"
    except Exception as e:
        raise Exception(
            f"Failed to download {remote_file_name} from {GOOGLE_CLOUD_STORAGE_BUCKET} bucket, error: {str(e)}"
        )


def upload_video_to_google_cloud_storage(file_to_upload_name):
    try:
        storage_manager = GoogleCloudStorageManager(GOOGLE_CLOUD_STORAGE_BUCKET)
        local_path = f"{ASSETS_PATH}/{VIDEO_FOLDER_NAME}/{file_to_upload_name}"
        storage_manager.upload_file_by_file_name(local_path, file_to_upload_name)
        return f"File {file_to_upload_name} uploaded successfully to: {GOOGLE_CLOUD_STORAGE_BUCKET} bucket"
    except Exception as e:
        raise Exception(
            f"Failed to upload {file_to_upload_name} to {GOOGLE_CLOUD_STORAGE_BUCKET} bucket, error: {str(e)}"
        )


def publish_message_to_pub_sub_error_topic(task):
    try:
        task_id = task["task_id"]
        pubsub_manager = PubSubManager()
        topic_path = GOOGLE_CLOUD_PUB_SUB_TOPIC_ERROR_PATH
        data = f"Processing task: {task_id}"
        message_published_id = pubsub_manager.publish_message(topic_path, data, **task)
        message = f"Message published in {GOOGLE_CLOUD_PUB_SUB_TOPIC_ERROR_PATH} topic with id: {message_published_id}"
        print(f"\n{message}\n")
        return message
    except Exception as e:
        raise Exception(f"Error publishing message: {str(e)}")
