from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import (
    UUIDType,
    URLType,
)


db = SQLAlchemy()


class Tag(db.Model):

    __tablename__ = 'tag'

    object_id = db.Column('id', UUIDType(), primary_key=True, default=uuid4)
    value = db.Column(db.String(40))

    post = db.relationship('Post', backref='tags')
    post_id = db.Column(UUIDType(), db.ForeignKey('post.id'))

    def __str__(self) -> str:
        return f'Tag {self.value} on {self.post}'


class Reference(db.Model):

    __tablename__ = 'reference'

    object_id = db.Column('id', UUIDType(), primary_key=True, default=uuid4)
    url = db.Column(URLType)
    description = db.Column(db.String(300))

    post = db.relationship('Post', backref='references')
    post_id = db.Column(UUIDType(), db.ForeignKey('post.id'))

    def __str__(self) -> str:
        return f'Reference to {self.url} on {self.post}'


class Author(db.Model):

    __tablename__ = 'author'

    object_id = db.Column('id', UUIDType(), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    media_url = db.Column(URLType)
    organisation = db.Column(db.String(100))
    organisation_url = db.Column(URLType)

    def __str__(self) -> str:
        return f'Author {self.name}'


class Post(db.Model):

    __tablename__ = 'post'

    object_id = db.Column('id', UUIDType(), primary_key=True, default=uuid4)
    title = db.Column(db.String(100), nullable=False)
    date_published = db.Column(db.DateTime(timezone=True), nullable=False)
    date_written = db.Column(db.DateTime(timezone=True))
    summary = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    footer = db.Column(db.String(100), nullable=False)

    author = db.relationship('Author', backref='posts')
    author_id = db.Column(
        UUIDType(), 
        db.ForeignKey('author.id'),
        nullable=False
    )

    def __str__(self) -> str:
        return f'Post {self.title} by {self.author}'
