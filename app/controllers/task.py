from datetime import datetime
import json
import re
from flask import Blueprint, render_template, request
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import exc
from models.models import db, Task, TaskStatus, Video
from config.global_constants import (
    VALID_VIDEO_EXTENSIONS,
)
from controllers.utils import (
    generate_google_cloud_storage_signed_url,
    publish_message_to_pub_sub,
    upload_video_to_google_cloud_storage,
)
from pathlib import Path

task_bp = Blueprint("task", __name__)


@task_bp.route("/task", methods=["POST"])
@jwt_required()
def create_task():
    file = request.files.get("file")

    file_extension_validation = Path(file.filename).suffix in VALID_VIDEO_EXTENSIONS

    if not file:
        return {"message": "No se cargo ningún archivo"}, 400

    if not file_extension_validation:
        valid_extensions_str = ", ".join(VALID_VIDEO_EXTENSIONS)
        return {
            "message": f"Extensión no compatible, solo se admiten archivos ({valid_extensions_str})"
        }, 415

    try:
        user_id = current_user.id

        video = Video(
            status=TaskStatus.UPLOADED.value,
            raiting=0,
            id_user=user_id,
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

        filename = f"user_{user_id}_video_{video.id}_original.mp4"
        upload_video_to_google_cloud_storage(file, filename)

        response = {
            "video_id": str(video.id),
            "task_id": str(task.id),
            "user_id": str(user_id),
        }
        publish_message_id = publish_message_to_pub_sub(response)
        response["publish_message_id"] = publish_message_id

        return {"message": response}, 200
    except json.JSONDecodeError as e:
        return {"message": "Datos JSON no válidos"}, 400
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Error al crear objetos: {str(e)}"}, 500
    except Exception as e:
        return {"message": str(e)}, 500


@task_bp.route("/task", methods=["GET"])
@jwt_required()
def get_task_by_user():
    try:
        max_results = request.args.get("max", default=None, type=int)
        order = request.args.get("order", default=0, type=int)

        tasks_query = Task.query.filter(Task.id_user == current_user.id)

        if order == 1:
            tasks_query = tasks_query.order_by(Task.id.desc())
        else:
            tasks_query = tasks_query.order_by(Task.id.asc())

        if max_results is not None:
            tasks_query = tasks_query.limit(max_results)

        tasks = tasks_query.all()

        serialized_tasks = []
        for task in tasks:
            serialized_task = {
                "id": task.id,
                "timestamp": task.timestamp.isoformat(),
                "status": task.status.value,
                "id_video": task.id_video,
                "id_user": task.id_user,
            }
            serialized_tasks.append(serialized_task)

        return {"message": serialized_tasks}, 200
    except exc.SQLAlchemyError as e:
        return {"message": f"Error al recuperar las tareas del usuario: {str(e)}"}, 500
    except Exception as e:
        return {"message": str(e)}, 500


@task_bp.route("/task/worker_logs", methods=["GET"])
@jwt_required()
def get_worker_logs():
    try:
        with open("video_processor_worker/logs.txt", "r") as file:
            logs_content = file.read()
        logs_entries = re.split(r"\n\s*\n", logs_content.strip())

        if not logs_content.strip():
            return {"message": "El archivo logs.txt está vacío"}, 200

        return render_template("logs.html", logs_entries=logs_entries)

    except FileNotFoundError:
        return {"message": "El archivo logs.txt no se encontró"}, 404
    except Exception as e:
        print(e)
        return {"message": str(e)}, 500


@task_bp.route("/task/<int:id>", methods=["GET"])
@jwt_required()
def get_task_by_id(id):
    try:
        task = Task.query.filter_by(id=id, id_user=current_user.id).first()
        if not task:
            return {"message": "Tarea no encontrada"}, 404

        video = Video.query.filter_by(id=task.id_video).first()

        if not video:
            return {"message": "Video no encontrado"}, 404

        download_url = ""

        if video.edited_url != None:
            download_url = generate_google_cloud_storage_signed_url(video.edited_url)

        serialized_task = {
            "id": task.id,
            "timestamp": task.timestamp.isoformat(),
            "status": task.status.value,
            "id_video": task.id_video,
            "id_user": task.id_user,
            "download_url": download_url,
        }
        return {"message": serialized_task}, 200
    except exc.SQLAlchemyError as e:
        return {"message": f"Error al obtener la tarea: {str(e)}"}, 500
    except Exception as e:
        return {"message": str(e)}, 500


@task_bp.route("/task/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task_by_id(id):
    try:
        task = Task.query.filter_by(id=id, id_user=current_user.id).first()

        if not task:
            return {"message": "Tarea no encontrada"}, 404
        elif task.status.value == TaskStatus.UPLOADED.value:
            return {
                "message": f"La tarea con status ({TaskStatus.UPLOADED.value}), no puede ser eliminada"
            }, 405

        db.session.delete(task)
        db.session.commit()

        return {"message": "Tarea eliminada correctamente"}, 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Error al eliminar la tarea: {str(e)}"}, 500
    except Exception as e:
        return {"message": str(e)}, 500
