from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_login import current_user
from .models import User

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(label='Current Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    new_password = PasswordField(label='New Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    confirm_password = PasswordField(label='Confirm New Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    submit = SubmitField("Change password")


    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Incorrect current password. Please try again.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_photo = FileField('Upload a new profile picture', validators=[
    FileAllowed(['jpg', 'png'], 'Only files with the extension .jpg or .png are allowed.')])
    about_me = StringField('About Me', validators=[Length(max=140)])
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


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