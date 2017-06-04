from flask import Flask
from flask_cors import CORS

from tal.api.models import db
from tal.api.rest import rest


app = Flask(__name__)
CORS(app, origins=('*',))

app.config.from_pyfile('../config.py')

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(rest)
