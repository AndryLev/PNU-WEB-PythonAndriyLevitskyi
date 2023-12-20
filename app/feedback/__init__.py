from flask import Blueprint

feedback_blueprint = Blueprint('feedback', __name__, template_folder="templates", url_prefix="/feedback")

from . import views