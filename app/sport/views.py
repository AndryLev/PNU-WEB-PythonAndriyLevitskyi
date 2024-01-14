from flask_restful import Resource
from flask import request
from app import db
from .models import SportEvent
from .schemas.sport import SportEventSchema
from app.auth_api.views import required_token_second

class SportEventsApi(Resource):
    def get(self):
        schema = SportEventSchema(many=True)
        sport_events = SportEvent.query.all()
        return {"sport_events": schema.dump(sport_events)}

    @required_token_second
    def post(self):
        schema = SportEventSchema()

        sport_event = schema.load(request.json)

        db.session.add(sport_event)
        db.session.commit()

        return {"sport_event": schema.dump(sport_event)}, 201


class SportEventResource(Resource):
    @required_token_second
    def get(self, id):
        schema = SportEventSchema()
        sport_event = SportEvent.query.get_or_404(id)
        return {"sport_event": schema.dump(sport_event)}

    @required_token_second
    def put(self, id):
        schema = SportEventSchema()
        sport_event = SportEvent.query.get_or_404(id)

        sport_event = schema.load(request.json, instance=sport_event)
        db.session.commit()

        return {"sport_event": schema.dump(sport_event)}

    @required_token_second
    def delete(self, id):
        schema = SportEventSchema()
        sport_event = SportEvent.query.get_or_404(id)

        db.session.delete(sport_event)
        db.session.commit()

        return {"sport_event": schema.dump(sport_event), "message": f"Sport event {sport_event.name} deleted"}


