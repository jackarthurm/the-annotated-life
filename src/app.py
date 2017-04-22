from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.rest import rest


app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(rest)

db = SQLAlchemy(app)
db.create_all()


