from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import (
    UUIDType,
    URLType,
)


db = SQLAlchemy()


class SaveModelMixin(object):

    def save(self):
        db.session.add(self)
        db.session.commit()


class Tag(SaveModelMixin, db.Model):

    __tablename__ = 'tag'

    id_ = db.Column('id', db.Integer, primary_key=True)
    value = db.Column(db.String(40))

    post = db.relationship('Post', backref='tags')
    post_id = db.Column(UUIDType(), db.ForeignKey('post.uuid'))

    def __repr__(self):
        return '{self.__name__} {self.id_}'.format(self=self)

    def __str__(self):
        return 'Tag {self.value} on {self.post}'.format(self=self)


class Reference(SaveModelMixin, db.Model):

    __tablename__ = 'reference'

    id_ = db.Column('id', db.Integer, primary_key=True)
    url = db.Column(URLType)
    description = db.Column(db.String(300))

    post = db.relationship('Post', backref='references')
    post_id = db.Column(UUIDType(), db.ForeignKey('post.uuid')) 

    def __repr__(self):
        return '{self.__name__} {self.id}'.format(self=self) 

    def __str__(self):
        return 'Reference to {self.url} on {self.post}'.format(self=self)


class Author(SaveModelMixin, db.Model):

    __tablename__ = 'author'    

    uuid = db.Column(UUIDType(), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    media_url = db.Column(URLType)
    organisation = db.Column(db.String(100))
    organisation_url = db.Column(URLType)

    def __repr__(self):
        return '{self.__name__} {self.uuid}'.format(self=self)

    def __str__(self):
        return 'Author {self.name}'.format(self=self)


class Post(SaveModelMixin, db.Model):

    __tablename__ = 'post'

    uuid = db.Column(UUIDType(), primary_key=True, default=uuid4)
    title = db.Column(db.String(100), nullable=False)
    date_published = db.Column(db.DateTime, nullable=False)
    date_written = db.Column(db.DateTime)
    summary = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    footer = db.Column(db.String(100))

    author = db.relationship('Author', backref='posts')
    author_id = db.Column(
        UUIDType(), 
        db.ForeignKey('author.uuid'), 
        nullable=False
    )

    def __repr__(self):
        return '{self.__name__} {self.uuid}'.format(self=self)

    def __str__(self):
        return 'Post {self.title} by {self.author}'.format(self=self)
