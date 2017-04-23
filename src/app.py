from flask import Flask

from src.models import db
from src.rest import rest


app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(rest)
