from ..database import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_person = db.Column(db.Integer, db.ForeignKey('person.id'))
    model = db.Column(db.String(10), unique=False, nullable=True)
    color = db.Column(db.String(10), unique=False, nullable=True)
    tag = db.Column(db.String(10), unique=False, nullable=True)
