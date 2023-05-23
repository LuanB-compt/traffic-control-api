import serial
import datetime
from .controller.car import CarController
from .controller.person import PersonController
from .data.models.Car import Car

carCtrl = CarController()
personCtrl = PersonController()


def check_license(tag: str):
    car = carCtrl.find_by_tag(tag)
    if car is not None:
        if car.expiration is not None:
            if car.expiration >= datetime.datetime.now().date():
                return (True, car)
            else:
                return (False, None)
        return (True, car)
    return (False, None)


def get_info(car: Car):
    owner = personCtrl.find_by_id(car.id_person)
    return {
        "status": 1,
        "vehicle": f"{car.brand} {car.model} {car.color} - {car.year}",
        "license": car.tag,
        "owner": owner.name if owner is not None else "Não informado",
        "entry": datetime.datetime.now().strftime("%m/%d/%Y %H:%M"),
    }
