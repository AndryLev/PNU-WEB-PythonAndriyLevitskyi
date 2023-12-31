from flask import Blueprint

auth_api_blueprint = Blueprint("auth_api", __name__, url_prefix="/auth_api")

from . import views