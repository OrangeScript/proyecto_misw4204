from sqlalchemy import exc
from flask import request
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource

from modelos import db, User, UserSchema

user_schema = UserSchema()

class VistaSignIn(Resource):

    def post(self):

        new_usuar = User(
            new_user = request.json['user'], password=request.json['password']
        )

        db.session.add(new_usuar)

        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return {"mensaje": "Ya existe un usuario con este identificador"}, 400
        
        access_token = create_access_token(identity=new_usuar.id)
        return {"mensaje": "Administrador creado", "token": access_token, "id": access_token.id}, 201
    
    @jwt_required()
    def put(self, id_usuario):
        user_token = current_user
        if id != current_user.id:
            return {'mensaje': 'Peticion invalida'}, 400
        user_token.password = request.json.get(
            "password", user_token.password
        )
        db.session.commit()
        return user_schema.dump(user_token)