from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.data import posts
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app import models
with app.app_context():
    db.create_all()
from app import views

