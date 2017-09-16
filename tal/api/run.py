from tal.api.app_factory import create_app
from tal.api.models import db


app = create_app()

with app.app_context():
    db.create_all()

app.run()
