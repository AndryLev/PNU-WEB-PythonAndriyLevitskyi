from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from .views import UsersApi, UserApi

users_api_blueprint = Blueprint("users_api", __name__, url_prefix="/api")
api = Api(users_api_blueprint)

api.add_resource(UsersApi, "/users")
api.add_resource(UserApi, "/users/<int:id>")


@users_api_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400