from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.complete,
        }