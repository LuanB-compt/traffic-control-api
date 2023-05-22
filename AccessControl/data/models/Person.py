from ..database import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    phone = db.Column(db.String(11), unique=False, nullable=True)
    homeNumber = db.Column(db.Integer, unique=False, nullable=True)
    address = db.Column(db.String(200), unique=False, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "homeNumber": self.homeNumber,
            "address": self.address,
        }
