import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'secret'
SESSION_PERMANENT = True


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance/feedback.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False