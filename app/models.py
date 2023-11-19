from app import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    feedback_text = db.Column(db.Text)

    def __init__(self, name, feedback_text):
        self.name = name
        self.feedback_text = feedback_text
