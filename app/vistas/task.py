from datetime import datetime
import json
import os
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import exc
from modelos.modelos import db, Task, TaskStatus, Video
from config.global_constants import (
    ASSETS_PATH,
    VALID_VIDEO_EXTENSIONS,
    VIDEO_FOLDER_NAME,
)
from vistas.utils import (
    download_video_from_ftp_server,
    send_message_to_RabbitMQ,
    upload_file_ftp,
)
from pathlib import Path

task_bp = Blueprint("task", __name__)


@task_bp.route("/task", methods=["POST"])
@jwt_required()
def create_task():
    file = request.files.get("file")

    file_extension_validation = Path(file.filename).suffix in VALID_VIDEO_EXTENSIONS

    if not file:
        return {"message": "No file provided"}, 400

    if not file_extension_validation:
        valid_extensions_str = ", ".join(VALID_VIDEO_EXTENSIONS)
        return {
            "message": f"Unsupported extension, only ({valid_extensions_str}) files"
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

        upload_file_ftp(file, filename)

        response = {
            "video_id": video.id,
            "task_id": task.id,
            "user_id": user_id,
        }

        send_message_to_RabbitMQ(response)

        return {"message": response}, 200
    except json.JSONDecodeError as e:
        return {"message": "Invalid JSON data"}, 400
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Error creating objects: {str(e)}"}, 500


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
        return {"message": f"Error al obtener las tareas del usuario: {str(e)}"}, 500


@task_bp.route("/task/download/<path:filename>", methods=["GET"])
def download_file(filename):
    try:
        download_video_from_ftp_server(filename)
        file_path = f"{ASSETS_PATH}/{VIDEO_FOLDER_NAME}/{filename}"
        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)
        return response, 200
    except FileNotFoundError:
        return jsonify({"message": "File not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


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

        base_url = request.url_root
        download_url = ""

        if video.edited_url != None:
            download_url = f"{base_url}api/task/download/{video.edited_url}"

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


@task_bp.route("/task/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task_by_id(id):
    try:
        task = Task.query.filter_by(id=id, id_user=current_user.id).first()

        if not task:
            return {"message": "Tarea no encontrada"}, 404
        elif task.status.value == TaskStatus.UPLOADED.value:
            return {
                "message": f"Tarea con status {TaskStatus.UPLOADED.value}, no puede ser eliminada"
            }, 405

        db.session.delete(task)
        db.session.commit()

        return {"message": "Tarea eliminada correctamente"}, 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Error al eliminar la tarea: {str(e)}"}, 500
