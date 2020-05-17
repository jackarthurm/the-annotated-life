from flask import Flask

from tal.api.app_factory import create_app

application: Flask = create_app()
