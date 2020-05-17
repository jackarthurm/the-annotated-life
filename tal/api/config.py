import os
from typing import (
    Dict,
    List,
    Optional,
)

from tal.api.tal_types import DatabaseURI


BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))

database_uri: Optional[DatabaseURI] = os.environ.get('DB_URI')

if database_uri is None:

    database_config: Dict[str, str] = dict(
        role=os.environ['DB_ROLE'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        name=os.environ['DB_NAME'],
    )

    database_uri: DatabaseURI = (
        'postgres://{role}:{password}@{host}:{port}/{name}'.format(
            **database_config
        )
    )

SQLALCHEMY_DATABASE_URI: DatabaseURI = database_uri

SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

CSRF_ENABLED: bool = True

CSRF_SESSION_KEY: str = os.environ['CSRF_SESSION_KEY']

SECRET_KEY: str = os.environ['SECRET_KEY']

SERVER_NAME: str = os.environ['SERVER_NAME']

JSON_AS_ASCII: bool = False

PAGE_SIZE: int = 20


# Must be provided as a CSV string
cors_allowed_origins: str = os.environ['CORS_ALLOWED_ORIGINS']

CORS_ALLOWED_ORIGINS: List[str] = list(
    filter(None, [o.strip() for o in cors_allowed_origins.split(',')])
)
