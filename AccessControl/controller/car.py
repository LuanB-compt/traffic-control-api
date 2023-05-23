from ..data.database import db
from ..data.models import Car
import datetime

class CarController():
    def __init__(self):
        pass

    def create(self, request: dict, id_person: int) -> Car.Car:
        new_car = Car.Car(
            id_person = id_person,
            model = request['model'],
            color = request['color'],
            tag = request['tag'],
            brand = request['brand'],
            year = request['year'],
            expiration = datetime.datetime.strptime(request['expiration'], "%Y-%m-%d")
        )
        db.session.add(new_car)
        db.session.flush()
        db.session.commit()
        print(f"\n- Created the {new_car.id} user in database\n")
        return new_car.to_dict()

    def read(self, id : int or None = None) -> any:
        if type(id) == int:
            return db.session.query(Car.Car).filter(Car.Car.id == id).first().to_dict()
        cars = db.session.query(Car.Car)
        return [car.to_dict() for car in cars]
    
    def update(self, request: dict) -> bool:
        try:
            car = db.session.query(Car.Car).filter(
                Car.Car.id == request['id']
            ).first()
            car.id_person = request['id_person'],
            car.model = request['model'],
            car.color = request['color'],
            car.tag = request['tag']
            db.session.commit()
            print(f"\n- Updated the {request['id']} Metadata in database\n")
            return True
        except:
            return False

    def delete(self, id: int) -> bool:
        try:
            delete = db.session.query(Car.Car).filter(Car.Car.id == id).first()
            db.session.delete(delete)
            return True
        except:
            return False

    def find_by_tag(self, tag: str) -> Car.Car:
        return db.session.query(Car.Car).filter(Car.Car.tag == tag).first()