import os
import json
import subprocess
from config.global_constants import (
    ASSETS_PATH,
    FTP_ADMIN_USER,
    FTP_PASSWORD,
    FTP_REMOTE_SERVER,
    FTP_VIDEOS_FOLDER,
    LOGO_NAME,
    LOGO_FOLDER_NAME,
    LOGO_VIDEO_ITEM_NAME,
    GLOBAL_VIDEO_SIZE,
    VIDEO_FOLDER_NAME,
)
from ftplib import FTP


def check_file_existence(file_path):
    try:
        if os.path.exists(file_path):
            return True
        else:
            return False
    except Exception as e:
        raise RuntimeError(f"\nError checking file existence: {e}")


def remove_file(file_path):
    if check_file_existence(file_path):
        try:
            os.remove(file_path)
            return f"Removed: {file_path}"
        except Exception as e:
            raise Exception(f"\nError removing file {file_path}: {e}")
    else:
        return f"\nFile {file_path} does not exist."


def get_asset_path(type, name):
    try:
        project_path = "assets/"
        return f"{project_path}{type}/{name}"
    except Exception as e:
        raise RuntimeError(f"\nError getting asset path: {e}")


def create_logo_video():
    output_logo_video_path = get_asset_path(LOGO_FOLDER_NAME, LOGO_VIDEO_ITEM_NAME)
    logo_path = get_asset_path(LOGO_FOLDER_NAME, LOGO_NAME)
    try:
        subprocess.run(
            [
                "ffmpeg",
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


def add_process_logs(logs):
    log_file_path = "logs.txt"
    if not check_file_existence(log_file_path):
        with open(log_file_path, "w") as file:
            pass

    with open(log_file_path, "a") as file:
        file.write("\n")
        for log in logs:
            file.write(log + "\n")


def download_video_from_ftp_server(remote_file_name):
    try:
        ftp = FTP(FTP_REMOTE_SERVER)
        ftp.login(user=FTP_ADMIN_USER, passwd=FTP_PASSWORD)
        ftp.cwd(FTP_VIDEOS_FOLDER)
        local_path = f"{ASSETS_PATH}/{VIDEO_FOLDER_NAME}/{remote_file_name}"
        with open(local_path, "wb") as file:
            ftp.retrbinary(f"RETR {remote_file_name}", file.write)
        ftp.quit()
        return f"File {remote_file_name} downloaded successfully to: {local_path}"
    except Exception as e:
        raise Exception(
            f"Failed to download {remote_file_name} from {FTP_VIDEOS_FOLDER}, error: {str(e)}"
        )


def upload_video_to_ftp_server(file_to_upload_name):
    try:
        with FTP(FTP_REMOTE_SERVER) as ftp:
            ftp.login(FTP_ADMIN_USER, FTP_PASSWORD)
            if FTP_VIDEOS_FOLDER not in ftp.nlst():
                ftp.mkd(FTP_VIDEOS_FOLDER)

            ftp.cwd(FTP_VIDEOS_FOLDER)

            local_path = f"{ASSETS_PATH}/{VIDEO_FOLDER_NAME}/{file_to_upload_name}"

            with open(local_path, "rb") as file:
                ftp.storbinary(f"STOR {file_to_upload_name}", file)

            return f"File {file_to_upload_name} uploaded successfully to: {FTP_VIDEOS_FOLDER}/{file_to_upload_name}"
    except Exception as e:
        raise Exception(
            f"Failed to upload {file_to_upload_name} from {FTP_VIDEOS_FOLDER}, error: {str(e)}"
        )


def create_error_log(error_type, error_message, timestamp_str):
    error_log = {
        "error_type": error_type,
        "message": error_message,
        "timestamp": timestamp_str,
    }
    return json.dumps(error_log)
