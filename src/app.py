from flask import Flask
from flask_sqlalchemy import SQLALchemy


app = Flask(__name__)
app.config_from_object('config')

db = SQLAlchemy(app)

db.create_all()



