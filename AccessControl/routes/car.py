import flask as fl
from ..controller.car import CarController
from ..controller.person import PersonController

bp = fl.Blueprint(name="car_routes", url_prefix="/car", import_name=__name__)
car = CarController()
person = PersonController()

@bp.route("/", methods=["POST"], strict_slashes=False)
def create():
    req = fl.request.get_json()
    owner = person.find_by_name(req['owner'])
    if owner:
        id_person = owner.id
    else:
        id_person = None

    new = car.create(req, id_person)
    if new:
        return fl.jsonify(new), 201
    else:
        return "New car could not be created", 500

@bp.route("/", methods=["GET"], strict_slashes=False)
def read():
    cars = car.read()
    if cars:
        return cars, 200
    else:
        return "Users is empty", 404

@bp.route("/<int:id>", methods=["GET"])
def read_id(id: int):
    car_found = car.read(id)
    if car_found:
        return car_found, 200
    else:
        return "Car not found", 404

@bp.route("/update/<int:id>", methods=["POST"])
def update(id: int):
    pass

bp.route("/delete/<int:id>", methods=["DELETE"])
def delete(id: int):
    pass