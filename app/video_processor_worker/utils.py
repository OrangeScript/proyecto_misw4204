import os
import subprocess
from config.global_constants import (
    LOGO_NAME,
    LOGO_FOLDER_NAME,
    LOGO_VIDEO_ITEM_NAME,
    GLOBAL_VIDEO_SIZE,
)


def check_file_existence(file_path):
    try:
        if os.path.exists(file_path):
            return True
        else:
            return False
    except Exception as e:
        print(f"\nError checking file existence: {e}")
        return False


def remove_file(file_path):
    if check_file_existence(file_path):
        try:
            os.remove(file_path)
            return True
        except OSError as e:
            print(f"\nError removing file {file_path}: {e}")
            return False
    else:
        print(f"\nFile {file_path} does not exist.")
        return False


def get_asset_path(type, name):
    try:
        project_path = "assets/"
        return f"{project_path}{type}/{name}"
    except Exception as e:
        print(f"\nError getting asset path: {e}")
        return None


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
        print(f"{LOGO_VIDEO_ITEM_NAME} created...")
    except Exception as e:
        print(f"\nError creating logo video: {e}")


def add_process_logs(logs):
    log_file_path = "logs.txt"
    if not check_file_existence(log_file_path):
        with open(log_file_path, "w") as file:
            pass

    with open(log_file_path, "a") as file:
        file.write("\n")
        for log in logs:
            file.write(log + "\n")
