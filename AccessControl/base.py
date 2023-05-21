import flask as fl
import flask_cors
from .routes import car, person, predict
from .data.database import db
from .config import Config

def create_app():
    app = fl.Flask(__name__)

    app.config.from_object(obj=Config)
    app.register_blueprint(blueprint=car.bp)
    app.register_blueprint(blueprint=person.bp)
    
    db.init_app(app=app)
    with app.app_context():
        db.create_all()
        flask_cors.CORS(app=app)
        return app
