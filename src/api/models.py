from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Post(db.Model):

    uuid = db.Column(db.Integer,
                     primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)