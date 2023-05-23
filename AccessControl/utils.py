import time
import serial
import datetime
import threading
from .controller.car import CarController
from .controller.person import PersonController
from .data.models.Car import Car

# Configurações da porta serial
serial_port = 'COM4'  # Altere para a porta serial correta
baud_rate = 9600
delay = 10 #seconds

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


def get_info(car: Car, entry):
    owner = personCtrl.find_by_id(car.id_person)
    return {
        "status": 1,
        "vehicle": f"{car.brand} {car.model} {car.color} - {car.year}",
        "license": car.tag,
        "owner": owner.name if owner is not None else "Não informado",
        "entry": entry,
    }

def close_serial_message():
    time.sleep(delay)
    ser = serial.Serial(serial_port, baud_rate)
    print("closing")
    ser.write(b'0')
    ser.flush()
    ser.close()
    
tr = threading.Thread(target=close_serial_message)
def open_serial_message():
    if tr.is_alive():
        tr.join(timeout=0.1)
    ser = serial.Serial(serial_port, baud_rate)
    print("opening")
    ser.write(b'1')
    ser.flush()
    ser.close()
    tr.start()
    
