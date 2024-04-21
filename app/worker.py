import json
import subprocess
import sys
from moviepy import editor
import timeit
from datetime import datetime
from sqlalchemy import exc, orm, create_engine
from time import sleep
from modelos.modelos import Task, TaskStatus, Video
from config.global_constants import (
    RABBITMQ_HOST,
    RABBITMQ_QUEUE_NAME,
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
from video_processor_worker.rabbitMqConfig import RabbitMQ
from video_processor_worker.utils import (
    create_error_log,
    download_video_from_ftp_server,
    get_asset_path,
    create_logo_video,
    check_file_existence,
    remove_file,
    add_process_logs,
    upload_video_to_ftp_server,
)

if __name__ == "__main__":
    rabbitmq = RabbitMQ(RABBITMQ_HOST, RABBITMQ_QUEUE_NAME)
    rabbitmq.ensure_queue_exists()
    db_url = f"postgresql+pg8000://{SQL_USER}:{SQL_PWD}@{SQL_DOMAIN}/{SQL_DB}"

    engine = create_engine(db_url)

    print(f"\nDB connection stablish: [ {db_url} ]")

    Session = orm.sessionmaker(bind=engine)
    session = Session()

    is_in_develop = len(sys.argv) > 1 and sys.argv[1] == "dev"

    def process_message(body):
        function_time_start = timeit.default_timer()
        decoded_message = body.decode("utf-8")
        try:
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

            process_logs = [decoded_message, timestamp_str]

            message = json.loads(decoded_message)

            user_id = message["user_id"]
            task_id = message["task_id"]
            video_id = message["video_id"]

            print("\nProcessing message:", message)

            ORIGINAL_VIDEO_NAME = f"user_{user_id}_video_{video_id}_original.mp4"
            EDITED_VIDEO_NAME = f"user_{user_id}_video_{video_id}_edited.mp4"

            process_logs.append(download_video_from_ftp_server(ORIGINAL_VIDEO_NAME))

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
                "-i",
                logo_video_path,
                "-i",
                output_aux_video_path,
                "-i",
                logo_video_path,
                "-filter_complex",
                "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]",
                "-map",
                "[outv]",
                "-map",
                "[outa]",
                output_video_path,
            ]

            subprocess.run(ffmpeg_command)

            process_logs.append(upload_video_to_ftp_server(EDITED_VIDEO_NAME))

            process_logs.append(remove_file(output_aux_video_path))

            if not is_in_develop:
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

        except exc.SQLAlchemyError as e:
            error_msg = f"Error creating objects: {str(e)}"
            print(error_msg)
            process_logs.append(
                create_error_log("SQLAlchemyError", error_msg, timestamp_str)
            )
            session.rollback()

        except json.JSONDecodeError as e:
            error_msg = f"Error decoding message: {decoded_message}, {str(e)}"
            print(error_msg)
            process_logs.append(
                create_error_log("JSONDecodeError", error_msg, timestamp_str)
            )

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

    rabbitmq.start_consuming(process_message)

    while True:
        pass
