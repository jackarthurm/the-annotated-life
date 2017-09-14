from flask import Flask
from flask_cors import CORS

from tal.api.models import db
from tal.api.schemas import ma
from tal.api.rest import rest


def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('../config.py')

    db.init_app(app)
    ma.init_app(app)
    rest.init_app(app)

    with app.app_context():
        db.create_all()

    CORS(app, origins=('*',))


    return app


create_app().run()
