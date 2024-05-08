import json
import subprocess
from moviepy import editor
import timeit
from datetime import datetime
from sqlalchemy import exc, orm, create_engine
from google_cloud_services.pub_sub_manager import PubSubManager
from models.models import Task, TaskStatus, Video
from config.global_constants import (
    GOOGLE_CLOUD_PUB_SUB_CREDENTIALS,
    GOOGLE_CLOUD_PUB_SUB_SUBSCRIPTION_PATH,
    IS_IN_DEVELOP,
    LOGO_FOLDER_NAME,
    LOGO_VIDEO_ITEM_NAME,
    SQL_DB,
    SQL_DOMAIN,
    SQL_PWD,
    SQL_USER,
    VIDEO_FOLDER_NAME,
    OUTPUT_VIDEO_NAME,
    GLOBAL_VIDEO_SIZE,
)
from video_processor_worker.utils import (
    create_error_log,
    download_video_from_google_cloud_storage,
    get_asset_path,
    create_logo_video,
    check_file_existence,
    remove_file,
    add_process_logs,
    upload_video_to_google_cloud_storage,
)

if __name__ == "__main__":

    def process_message(message):
        task = message.attributes
        function_time_start = timeit.default_timer()
        try:
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

            task_id = task.get("task_id")
            user_id = task.get("user_id")
            video_id = task.get("video_id")

            process_logs = [
                timestamp_str,
                f"task_id: {task_id}, user_id: {user_id}, video_id: {video_id}",
            ]

            print(f"\nProcessing: {message}\n")

            ORIGINAL_VIDEO_NAME = f"user_{user_id}_video_{video_id}_original.mp4"
            EDITED_VIDEO_NAME = f"user_{user_id}_video_{video_id}_edited.mp4"

            process_logs.append(
                download_video_from_google_cloud_storage(ORIGINAL_VIDEO_NAME)
            )

            logo_video_path = get_asset_path(LOGO_FOLDER_NAME, LOGO_VIDEO_ITEM_NAME)
            input_video_path = get_asset_path(VIDEO_FOLDER_NAME, ORIGINAL_VIDEO_NAME)
            output_aux_video_path = get_asset_path(LOGO_FOLDER_NAME, OUTPUT_VIDEO_NAME)

            output_video_path = get_asset_path(VIDEO_FOLDER_NAME, EDITED_VIDEO_NAME)

            clip = editor.VideoFileClip(input_video_path)
            duration_seconds = clip.duration

            if not check_file_existence(logo_video_path):
                process_logs.append(create_logo_video())

            if duration_seconds > 20:
                reduce_time_and_size_command = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    input_video_path,
                    "-t",
                    "18",
                    "-vf",
                    f"scale={GLOBAL_VIDEO_SIZE},setsar=1:1",
                    output_aux_video_path,
                ]
                subprocess.run(reduce_time_and_size_command)
                process_logs.append("Shortened and reduced video")

            else:
                command = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    input_video_path,
                    "-vf",
                    f"scale={GLOBAL_VIDEO_SIZE}",
                    output_aux_video_path,
                ]
                subprocess.run(command)
                process_logs.append("Reduced video")

            ffmpeg_command = [
                "ffmpeg",
                "-y",
                "-i",
                logo_video_path,
                "-i",
                output_aux_video_path,
                "-i",
                logo_video_path,
                "-filter_complex",
                "[0:v][1:v][2:v]concat=n=3:v=1:a=0[vv]",
                "-map",
                "[vv]",
                "-c:v",
                "libx264",
                "-profile:v",
                "high444",
                "-level",
                "4.1",
                "-r",
                "30",
                "-movflags",
                "+faststart",
                output_video_path,
            ]

            subprocess.run(ffmpeg_command)

            process_logs.append(upload_video_to_google_cloud_storage(EDITED_VIDEO_NAME))

            process_logs.append(remove_file(output_aux_video_path))

            if not IS_IN_DEVELOP:
                process_logs.append(remove_file(input_video_path))
                process_logs.append(remove_file(output_video_path))

            task = session.query(Task).get(task_id)
            video = session.query(Video).get(video_id)

            if task is None and video is None:
                process_logs.append(
                    f"Task with id {task_id} and Video with id {video_id} don't exist"
                )
            elif task is None:
                process_logs.append(f"Task with id {task_id} doesn't exist")
            elif video is None:
                process_logs.append(f"Video with id {video_id} doesn't exist")
            else:
                task.status = TaskStatus.PROCESSED.value
                video.status = TaskStatus.PROCESSED.value
                video.edited_url = EDITED_VIDEO_NAME
                session.commit()

            video_process_end_message = "Video processed..."
            print(video_process_end_message)
            process_logs.append(video_process_end_message)
            message.ack()

        except exc.SQLAlchemyError as e:
            error_msg = f"Error creating objects: {str(e)}"
            print(error_msg)
            process_logs.append(
                create_error_log("SQLAlchemyError", error_msg, timestamp_str)
            )
            session.rollback()

        except subprocess.CalledProcessError as e:
            error_msg = f"Error executing ffmpeg command: {str(e)}"
            print(error_msg)
            process_logs.append(
                create_error_log("CalledProcessError", error_msg, timestamp_str)
            )

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            process_logs.append(
                create_error_log("GeneralError", error_msg, timestamp_str)
            )
        finally:
            function_time_end = timeit.default_timer()
            time_calculus = function_time_end - function_time_start
            process_logs.insert(0, f"Execution time: {time_calculus}s")
            add_process_logs(process_logs)

    db_url = f"postgresql+pg8000://{SQL_USER}:{SQL_PWD}@{SQL_DOMAIN}/{SQL_DB}"

    engine = create_engine(db_url)

    print(f"\nDB connection stablish: [ {db_url} ]")

    Session = orm.sessionmaker(bind=engine)
    session = Session()

    pub_sub_subscription_path = GOOGLE_CLOUD_PUB_SUB_SUBSCRIPTION_PATH
    pubsub_manager = PubSubManager(GOOGLE_CLOUD_PUB_SUB_CREDENTIALS)

    print(f"\nListening messages from: [ {pub_sub_subscription_path} ]")

    pubsub_manager.listen_for_messages(
        pub_sub_subscription_path, callback=process_message
    )
