from flask import Flask
import service.config
from service.api.add_face import add_face_module
from service.api.check_person import check_person_module
from service.model import db
from service.model.face import Face
from service.model.log import Log


def create_app():
    app = Flask(__name__)
    app.config.from_object(service.config)
    app.register_blueprint(add_face_module)
    app.register_blueprint(check_person_module)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    return app

