from ..database import db
from .Person import Person

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_person = db.Column(db.Integer, db.ForeignKey(Person.id))
    year = db.Column(db.Integer, unique=False, nullable=True)
    model = db.Column(db.String(20), unique=False, nullable=True)
    brand = db.Column(db.String(20), unique=False, nullable=True)
    color = db.Column(db.String(10), unique=False, nullable=True)
    tag = db.Column(db.String(10), unique=True, nullable=False)
    expiration = db.Column(db.Date, unique=False, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_person": self.id_person,
            "model": self.model,
            "color": self.color,
            "tag": self.tag,
            "brand": self.brand,
            "year": self.year,
            "expiration": self.expiration
        }
