from app import db

class SportEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"SportEvent(id={self.id}, name={self.name}, date={self.date}, location={self.location})"