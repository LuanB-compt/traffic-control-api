import flask as fl

bp = fl.Blueprint(name="car_routes", import_name=__name__)

@bp.route("/create", methods=["POST"])
def create():
    pass

@bp.route("/read/", methods="GET")
def read():
    pass

@bp.route("/read/<int:id>", methods=["GET"])
def read_id(id: int):
    pass

@bp.route("/update/<int:id>", methods=["POST"])
def update(id: int):
    pass

bp.route("/delete/<int:id>", methods=["DELETE"])
def delete(id: int):
    pass