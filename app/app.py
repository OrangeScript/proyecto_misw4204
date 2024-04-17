import sys
import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from modelos import db
from modelos.modelos import User
from vistas.task import task_bp
from vistas.auth import auth_bp
from waitress import serve

try:
    load_dotenv('conf.env')
except FileNotFoundError:
    pass

app = Flask(__name__)

db_url = f"postgresql+pg8000://{os.environ['SQL_USER']}:{os.environ['SQL_PWD']}@{os.environ['SQL_DOMAIN']}/{os.environ['SQL_DB']}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "cloud"

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

if __name__ == "__main__":
    if sys.argv[1] == "dev":
        app.run(debug=True, host="0.0.0.0")
    else:
        serve(app=app, host='0.0.0.0', port="5000", threads=4)
