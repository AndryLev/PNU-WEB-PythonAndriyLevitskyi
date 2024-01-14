from marshmallow import fields, validate, validates_schema, ValidationError
from app import ma
from app.sport.models import SportEvent


class SportEventSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True, validate=[validate.Length(min=3, max=50)])
    date = fields.Date(required=True)
    location = fields.String(required=True, validate=[validate.Length(min=3, max=50)])

    @validates_schema
    def validate_email(self, data, **kwargs):
        name = data.get("name")
        if SportEvent.query.filter_by(name=name).first():
            raise ValidationError(f"Ця подія {name} вже записана")

    class Meta:
        model = SportEvent
        load_instance = True