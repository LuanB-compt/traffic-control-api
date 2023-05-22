from ..data.database import db
from ..data.models import Person


class PersonController:
    def __init__(self):
        pass

    def create(self, request: dict) -> Person.Person:
        new_person = Person.Person(
            name=request["name"],
            phone=request["phone"],
            homeNumber=request["homeNumber"],
            address=request["address"],
        )
        db.session.add(new_person)
        db.session.flush()
        db.session.commit()
        print(f"\n- Created the {new_person.id} user in database\n")
        return new_person.to_dict()

    def read(self, id: int or None = None) -> any:
        if id is not None:
            return (
                db.session.query(Person.Person).filter(Person.Person.id == id).first().to_dict()
            )
        people = db.session.query(Person.Person).all()
        return [person.to_dict() for person in people]
        
    def update(self, request: dict) -> bool:
        try:
            person = (
                db.session.query(Person.Person)
                .filter(Person.Person.id == request["id"])
                .first()
            )
            person.name = (request["name"],)
            person.phone = (request["phone"],)
            person.homeNumber = (request["homeNumber"],)
            person.quantVehicles = request["quantVehicles"]
            db.session.commit()
            print(f"\n- Updated the {request['id']} Metadata in database\n")
            return True
        except:
            return False

    def delete(self, id: int) -> bool:
        try:
            delete = (
                db.session.query(Person.Person).filter(Person.Person.id == id).first()
            )
            db.session.delete(delete)
            return True
        except:
            return False

    def find_by_name(self, name: str) -> Person:
        return db.session.query(Person.Person).filter_by(name=name).first()
