import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_URI = os.environ.get('DB_URI')

if DB_URI is None:

    DB_ROLE = os.environ['DB_ROLE']
    DB_PASS = os.environ['DB_PASS']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    DB_NAME = os.environ['DB_NAME']

    DB_URI = f'postgres://{DB_ROLE}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SQLALCHEMY_DATABASE_URI = DB_URI

THREADS_PER_PAGE = 2

CSRF_ENABLED = True

CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']
SECRET_KEY = os.environ['SECRET_KEY']