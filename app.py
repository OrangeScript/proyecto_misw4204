from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import db
from vistas.task import VistaTask

##"postgresql+pg8000://scott:tiger@localhost/test"

app = None

def create_flask_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@35.202.0.137/drl_cloud"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_context = app.app_context()
    app_context.push()
    add_urls(app)
    return app

def add_urls(app):
    api = Api(app)
    api.add_resource(VistaTask, '/api/task')

app = create_flask_app()
db.init_app(app)

try:
    db.create_all()
except:
    print('db exists')

if __name__ == '__main__':   
    app.run()