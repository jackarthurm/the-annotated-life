from src.app import db


class Post(db.Model):

    uuid = db.Column(db.Integer,
                     primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, 
                 title, 
                 body, 
                 pub_date=None):

        self.title = title