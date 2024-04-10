from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api


app = None

def create_flask_app():
    app = Flask(__name__)

    app_context = app.app_context()
    app_context.push()

    return app

app = create_flask_app()

if __name__ == '__main__':   
    app.run()