from sqlalchemy import exc
from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from modelos import db, User, UserSchema

user_schema = UserSchema()

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/signup", methods=["POST"])
def create_user():
    user_name = request.json["user"]
    email = request.json["email"]

    existing_user = User.query.filter(
        (User.user == user_name) | (User.email == email)
    ).first()

    if existing_user:
        return {
            "message": "Ya existe un usuario con este nombre o correo electrónico"
        }, 400

    new_user = User(
        user=user_name,
        email=email,
        password=request.json["password"],
    )

    db.session.add(new_user)

    try:
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        return {"message": f"Error de integridad en la base de datos: {str(e)}"}, 500

    access_token = create_access_token(identity=new_user.id)

    return {
        "message": access_token,
    }, 201


@auth_bp.route("/auth/login", methods=["POST"])
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
                "message": access_token,
            }, 200
        else:
            return {"message": "Verifique los datos ingresados"}, 404
    except KeyError as e:
        return {"message": f"Campo faltante: {str(e)}"}, 400
    except exc.SQLAlchemyError as e:
        return {"message": f"Error en la base de datos: {str(e)}"}, 500
