from sqlalchemy import exc
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, current_user, jwt_required

from modelos import db, User, UserSchema

user_schema = UserSchema()

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user_name = data["user"]
        password = data["password"]

        user = User.query.filter(
            User.user == user_name,
            User.password == password,
        ).first()

        if user:
            access_token = create_access_token(identity=user.id)
            return {
                "mensaje": access_token,
            }
        else:
            return {"mensaje": "Verifique los datos ingresados"}, 404
    except KeyError as e:
        return {"mensaje": f"Campo faltante: {str(e)}"}, 400
    except exc.SQLAlchemyError as e:
        return {"mensaje": f"Error en la base de datos: {str(e)}"}, 500
