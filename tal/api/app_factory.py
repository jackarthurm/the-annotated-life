from flask import Flask
from flask_cors import CORS

from tal.api.models import db
from tal.api.schemas import ma
from tal.api.rest import rest


app_module = '.'.join(__name__.split('.')[:-1])


def create_app():

    app = Flask(app_module)

    app.config.from_pyfile('config.py')

    db.init_app(app)
    ma.init_app(app)
    rest.init_app(app)

    CORS(app, origins=app.config['CORS_ALLOWED_ORIGINS'])

    return app

