import json
import subprocess
from moviepy import editor
from datetime import datetime
from sqlalchemy import exc, orm, create_engine

from modelos.modelos import Task, TaskStatus, Video
from video_processor_worker.constants import (
    HOST,
    QUEUE_NAME,
    LOGO_FOLDER_NAME,
    LOGO_VIDEO_ITEM_NAME,
    VIDEO_FOLDER_NAME,
    OUTPUT_VIDEO_NAME,
    GLOBAL_VIDEO_SIZE,
)
from video_processor_worker.rabbitMqConfig import RabbitMQ
from video_processor_worker.utils import (
    get_asset_path,
    create_logo_video,
    check_file_existence,
    remove_file,
    add_process_logs,
)

if __name__ == "__main__":
    rabbitmq = RabbitMQ(HOST, QUEUE_NAME)
    print("\nConnection stablish:", "[", HOST, "] [", QUEUE_NAME, "]")

    db_url = "postgresql+psycopg2://postgres:postgres@localhost/drl_cloud"

    """ db_url = "postgresql+psycopg2://postgres:postgres@35.202.0.137/drl_cloud" """

    engine = create_engine(db_url)

    print("\nDB connection stablish: ", db_url)

    Session = orm.sessionmaker(bind=engine)
    session = Session()

    def process_message(body):
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

            logo_video_path = get_asset_path(LOGO_FOLDER_NAME, LOGO_VIDEO_ITEM_NAME)
            input_video_path = get_asset_path(VIDEO_FOLDER_NAME, ORIGINAL_VIDEO_NAME)
            output_aux_video_path = get_asset_path(LOGO_FOLDER_NAME, OUTPUT_VIDEO_NAME)

            output_video_path = get_asset_path(VIDEO_FOLDER_NAME, EDITED_VIDEO_NAME)

            clip = editor.VideoFileClip(input_video_path)
            duration_seconds = clip.duration

            if not check_file_existence(logo_video_path):
                create_logo_video()

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
                "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]",
                "-map",
                "[v]",
                "-map",
                "[a]",
                output_video_path,
            ]

            subprocess.run(ffmpeg_command)

            remove_file(output_aux_video_path)

            task = session.query(Task).get(task_id)
            video = session.query(Video).get(video_id)

            if task is None or video is None:
                print("La tarea o el video no existen")
            else:
                task.status = TaskStatus.PROCESSED.value
                video.status = TaskStatus.PROCESSED.value
                video.edited_url = EDITED_VIDEO_NAME

                session.commit()

            process_logs.append("Video processed")

        except exc.SQLAlchemyError as e:
            session.rollback()
            process_logs.appendf(f"Error creating objects: {str(e)}")

        except json.JSONDecodeError as e:
            process_logs.append("Decoded message:", decoded_message)
        except subprocess.CalledProcessError as e:
            process_logs.append(f"Error executing FFmpeg command:{e}")

        add_process_logs(process_logs)

    rabbitmq.start_consuming(process_message)

    while True:
        pass
