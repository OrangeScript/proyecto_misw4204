from flask import Flask
from flask_jwt_extended import JWTManager
from modelos import db
from modelos.modelos import User
from vistas.task import task_bp
from vistas.auth import auth_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:postgres@35.202.0.137/drl_cloud"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "cloud"

jwt = JWTManager(app)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


app.register_blueprint(task_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

db.init_app(app)

try:
    db.create_all()
except:
    print("db exists")

if __name__ == "__main__":
    app.run()
