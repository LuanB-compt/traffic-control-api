import flask as fl
from ..utils import *

bp = fl.Blueprint(name="person_routes", url_prefix="/user", import_name=__name__)
person = personCtrl

@bp.route("/", methods=["POST"], strict_slashes=False)
def create():
    new = person.create(fl.request.get_json())
    if new:
        return fl.jsonify(new), 201
    else:
        return "New car could not be created", 500
    

@bp.route("/", methods=["GET"], strict_slashes=False)
def read():
    users = person.read()
    if users:
        return users, 200
    else:
        return "Users is empty", 404

@bp.route("/<int:id>", methods=["GET"])
def read_id(id: int):
    user = person.read(id)
    if user:
        return user, 200
    else:
        return "User is not found", 404

@bp.route("/update/<int:id>", methods=["UPDATE"])
def update(id: int):
    pass

bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    pass