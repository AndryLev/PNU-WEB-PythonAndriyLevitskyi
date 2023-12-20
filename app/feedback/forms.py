from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    feedback_text = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Send')