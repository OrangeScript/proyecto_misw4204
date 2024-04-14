from sqlalchemy import exc
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, current_user, jwt_required

from modelos import db, User, UserSchema

user_schema = UserSchema()

sign_in_bp = Blueprint("signin", __name__)


@sign_in_bp.route("/signin", methods=["POST"])
def create_user():
    new_user = User(
        user=request.json["user"],
        email=request.json["email"],
        password=request.json["password"],
    )

    db.session.add(new_user)

    try:
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        return {"mensaje": f"Error de integridad en la base de datos: {str(e)}"}, 500

    access_token = create_access_token(identity=new_user.id)

    return {
        "mensaje": access_token,
    }, 201


@sign_in_bp.route("/signin", methods=["GET"])
@jwt_required()
def get_user():
    print(current_user.id, current_user.user)
    return "yass", 200
