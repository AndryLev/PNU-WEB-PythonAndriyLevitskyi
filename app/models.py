from app import db
import bcrypt


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, pwd):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    feedback_text = db.Column(db.Text)

    def __init__(self, name, feedback_text):
        self.name = name
        self.feedback_text = feedback_text

