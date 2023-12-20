from flask import Blueprint

portfolio_blueprint = Blueprint('portfolio', __name__, template_folder="templates", url_prefix="/portfolio")

from . import views