from flask import Blueprint
from flask_restful import Api
from flask import jsonify
from .views import SportEventResource, SportEventsApi
from marshmallow import ValidationError

sport_events_api_bp = Blueprint("sport_events_api", __name__, url_prefix="/api")
api = Api(sport_events_api_bp)

api.add_resource(SportEventsApi, "/sport")
api.add_resource(SportEventResource, "/sport/<int:id>")

@sport_events_api_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400