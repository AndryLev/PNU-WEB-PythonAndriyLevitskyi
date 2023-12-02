from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError

from app.models import User

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    feedback_text = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Save')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="This field is required"), Length(min=4, max=20),
                                                   Regexp('^[a-zA-Z0-9_-]{3,20}$',
                                                          message='Invalid username. Use only letters, numbers, hyphens, or underscores.')])
    email = StringField('Email', validators=[DataRequired(message="This field is required"), Email(),
                                             Length(min=4, message='This field must contain a minimum of 6 characters')])
    password = PasswordField('Password', validators=[DataRequired(message='This field is required'),
                                                     Length(min=6, message='This field must contain a minimum of 6 characters')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message="This field is required"), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')