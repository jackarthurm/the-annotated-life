import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_URI = os.environ.get('DB_URI')

if DB_URI is None:

    DATABASE_CONFIG = {
    'role': os.environ['DB_ROLE'],
    'pass': os.environ['DB_PASS'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'name': os.environ['DB_NAME']
    }

    DB_URI = ('postgres://{role}:{pass}@{host}:{port}/{name}'
              .format(**DATABASE_CONFIG)
    )

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True

CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

SERVER_NAME = os.environ['SERVER_NAME']

JSON_AS_ASCII = False
