from flask import Flask

from tal.api.app_factory import create_app
from tal.api.models import db


app: Flask = create_app()

with app.app_context():
    db.create_all()

# Test code from here
from tal.api.models import Post, Author

author = Author(name='test name')
post = Post(
    author=author,
    body='test post body',
    title='Title',
    date_published='2007-04-05T12:30-02:00',
    summary='A summary'
)

with app.app_context():
    db.session.add(author)
    db.session.add(post)
    db.session.commit()

app.run()
