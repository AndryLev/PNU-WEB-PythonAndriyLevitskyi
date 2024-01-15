from os import environ, path
basedir = path.abspath(path.dirname(__file__))

class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret'
    FLASK_SECRET = SECRET_KEY
    WTF_CSRF_ENABLED = True
    SESSION_PERMANENT = True


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SESSION_PERMANENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'instance/feedback.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SESSION_PERMANENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'instance/feedback.db')

class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'instance/test.db')
    WTF_CSRF_ENABLED = False

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig
}