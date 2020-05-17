from flask import Flask
from flask_cors import CORS

from tal.api import urls
from tal.api.models import db


app_module: str = '.'.join(__name__.split('.')[:-1])


def create_app() -> Flask:

    app = Flask(app_module)

    app.config.from_pyfile('config.py')

    db.init_app(app)
    urls.init_app(app)

    CORS(app, origins=app.config['CORS_ALLOWED_ORIGINS'])

    return app
