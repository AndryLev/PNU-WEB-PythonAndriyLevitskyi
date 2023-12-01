from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    feedback_text = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Save')
