import enum
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


db = SQLAlchemy()

class TaskStatus(enum.Enum):

    UPLOADED = 'UPLOADED'
    PROCESSED = 'PROCESSED'

class User(db.Model):

    __table_args__ = (UniqueConstraint('user', name='unique_username'),)
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(128), nullable=False)
    edited_url = db.Column(db.String(128), nullable=False)
    raiting = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False)
    id_video = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)