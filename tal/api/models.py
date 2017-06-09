from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Post(db.Model):

  __tablename__ = 'post'


  uuid = db.Column(db.Integer,
                   primary_key=True)

  title = db.Column(db.String(100))
  pub_date = db.Column(db.DateTime)
  summary = db.Column(db.String(200))
  body = db.Column(db.Text)


