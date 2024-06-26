import enum
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class TaskStatus(enum.Enum):
    UPLOADED = "UPLOADED"
    PROCESSED = "PROCESSED"


class User(db.Model):
    __table_args__ = (UniqueConstraint("user", name="unique_username"),)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Worker_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    log_string = db.Column(db.String(1000), nullable=False)
    id_task = db.Column(db.Integer, nullable=True)
    id_user = db.Column(db.Integer, nullable=True)
    execution_time = db.Column(db.Float, nullable=True)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(128), nullable=False)
    edited_url = db.Column(db.String(128), nullable=True)
    raiting = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False)
    id_video = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        exclude = ("password",)


class VideoSchema(SQLAlchemyAutoSchema):
    id_user = fields.Integer()

    class Meta:
        model = Video
        include_relationships = True
        load_instance = True


class TaskSchema(SQLAlchemyAutoSchema):
    status = fields.Enum(TaskStatus, by_value=True)
    id_video = fields.Integer()
    id_user = fields.Integer()

    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
