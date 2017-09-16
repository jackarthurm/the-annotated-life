import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

database_uri = os.environ.get('DB_URI')

if database_uri is None:

    database_config = {
        'role': os.environ['DB_ROLE'],
        'pass': os.environ['DB_PASS'],
        'host': os.environ['DB_HOST'],
        'port': os.environ['DB_PORT'],
        'name': os.environ['DB_NAME'],
    }

    database_uri = (
        'postgres://{role}:{pass}@{host}:{port}/{name}'.format(
            **database_config
        )
    )

SQLALCHEMY_DATABASE_URI = database_uri

SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True

CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

SERVER_NAME = os.environ['SERVER_NAME']

JSON_AS_ASCII = False

PAGE_SIZE = 20


# Must be provided as a CSV string
cors_allowed_origins = os.environ['CORS_ALLOWED_ORIGINS']

CORS_ALLOWED_ORIGINS = list(
    filter(None, [o.strip() for o in cors_allowed_origins.split(',')])
)
