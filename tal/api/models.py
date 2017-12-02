from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import (
    UUIDType,
    URLType,
)


db = SQLAlchemy()


class SaveModelMixin(object):

    def save(self) -> None:
        db.session.add(self)
        return db.session.commit()


class Tag(SaveModelMixin, db.Model):

    __tablename__ = 'tag'

    id_ = db.Column('id', db.Integer, primary_key=True)
    value = db.Column(db.String(40))

    post = db.relationship('Post', backref='tags')
    post_id = db.Column(UUIDType(), db.ForeignKey('post.id'))

    def __str__(self) -> str:
        return f'Tag {self.value} on {self.post}'


class Reference(SaveModelMixin, db.Model):

    __tablename__ = 'reference'

    id_ = db.Column('id', db.Integer, primary_key=True)
    url = db.Column(URLType)
    description = db.Column(db.String(300))

    post = db.relationship('Post', backref='references')
    post_id = db.Column(UUIDType(), db.ForeignKey('post.id'))

    def __str__(self) -> str:
        return f'Reference to {self.url} on {self.post}'


class Author(SaveModelMixin, db.Model):

    __tablename__ = 'author'

    id = db.Column(UUIDType(), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    media_url = db.Column(URLType)
    organisation = db.Column(db.String(100))
    organisation_url = db.Column(URLType)

    def __str__(self) -> str:
        return f'Author {self.name}'


class Post(SaveModelMixin, db.Model):

    __tablename__ = 'post'

    id = db.Column(UUIDType(), primary_key=True, default=uuid4)
    title = db.Column(db.String(100), nullable=False)
    date_published = db.Column(db.DateTime(timezone=True), nullable=False)
    date_written = db.Column(db.DateTime(timezone=True))
    summary = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    footer = db.Column(db.String(100))

    author = db.relationship('Author', backref='posts')
    author_id = db.Column(
        UUIDType(), 
        db.ForeignKey('author.id'),
        nullable=False
    )

    def __str__(self) -> str:
        return f'Post {self.title} by {self.author}'
