from datetime import datetime
import json
import random
from flask import request
from sqlalchemy import exc
from flask_restful import Resource
from modelos.modelos import db, Task, TaskStatus, Video
from video_processor_worker.rabbitMqConfig import RabbitMQ
from vistas import constants
from vistas.utils import get_asset_path


class VistaTask(Resource):
    def post(self):
        file = request.files.get("file")

        if file:
            file_size = file.content_length
            MAX_VIDEO_SIZE_BYTES = 25 * 1024 * 1024

            if file_size > MAX_VIDEO_SIZE_BYTES:
                return {"mensaje": "File size exceeds the limit"}, 400

            try:
                user_id = random.randint(0, 100000)

                video = Video(
                    status=TaskStatus.UPLOADED.value, raiting=0, id_user=user_id
                )
                db.session.add(video)
                db.session.commit()

                timestamp = datetime.now()
                task = Task(
                    timestamp=timestamp,
                    status=TaskStatus.UPLOADED.value,
                    id_video=video.id,
                    id_user=user_id,
                )
                db.session.add(task)
                db.session.commit()

                VIDEO_FOLDER_NAME = constants.VIDEO_FOLDER_NAME
                filename = f"user_{user_id}_video_{video.id}_original.mp4"
                file_path = get_asset_path(VIDEO_FOLDER_NAME, filename)
                file.save(file_path)
                response = {
                    "video_id": video.id,
                    "task_id": task.id,
                    "user_id": user_id,
                }

                HOST = constants.HOST
                QUEUE = constants.QUEUE_NAME
                rabbitmq = RabbitMQ(HOST, QUEUE)
                rabbitmq.connect()
                rabbitmq.send_message(json.dumps(response), QUEUE)
                rabbitmq.close_connection()

                return {"mensaje": response}, 200
            except json.JSONDecodeError as e:
                return {"mensaje": "Invalid JSON data"}, 400
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                return {"mensaje": f"Error creating objects: {str(e)}"}, 500
        else:
            return "No file provided", 400
