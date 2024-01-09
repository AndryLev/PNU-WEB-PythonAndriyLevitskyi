from flask import request
from flask_restful import Resource
from app.auth.models import User
from app import db

from app.user_api.schemas.user import UserSchema


class UsersApi(Resource):
    def get(self):
        schema = UserSchema(many=True)
        users = User.query.all()

        return {"users": schema.dump(users)}

    def post(self):
        schema = UserSchema()

        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return {"user": schema.dump(user)}


class UserApi(Resource):
    def get(self, id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=id).first_or_404()

        if not user:
            return {"message": "Користувача не знайдено"}, 404
        return {"user": schema.dump(user)}

    def put(self, id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=id).first_or_404()

        user = schema.load(request.json, instance=user)
        db.session.add(user)
        db.session.commit()

        return {"user": schema.dump(user)}

    def delete(self, id):
        schema = UserSchema()
        user = User.query.filter_by(id=id).first()

        if not user:
            return {"message": "Користувача не знайдено"}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return {"user": schema.dump(user), "message": f"Користувач {user.username} видалений"}
        except Exception as e:
            db.session.rollback()
            return {"message": "Помилка видалення користувача", "error": str(e)}, 500