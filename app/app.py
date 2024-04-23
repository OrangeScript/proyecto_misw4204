import sys
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config.global_constants import (
    API_HOST,
    API_PORT,
    JWT_SECRET_KEY,
    SQL_DB,
    SQL_DOMAIN,
    SQL_PWD,
    SQL_USER,
)
from modelos import db
from modelos.modelos import User
from vistas.task import task_bp
from vistas.auth import auth_bp
from waitress import serve

app = Flask(__name__)

db_url = f"postgresql+pg8000://{SQL_USER}:{SQL_PWD}@{SQL_DOMAIN}/{SQL_DB}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024

app_context = app.app_context()
app_context.push()

app.register_blueprint(task_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

jwt = JWTManager(app)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


db.init_app(app)
db.create_all()


@app.route("/health")
def health_check():
    health_status = {"message": "ok"}
    return jsonify(health_status), 200


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        app.run(debug=True, host=API_HOST)
    else:
        print(f"* App started on: http://{API_HOST}:{API_PORT}")
        serve(app=app, host=API_HOST, port=API_PORT, threads=4)
