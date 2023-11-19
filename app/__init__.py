from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.data import posts

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'

db = SQLAlchemy(app)


with app.app_context():
    db.create_all()
from app import views

