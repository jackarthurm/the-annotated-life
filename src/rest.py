from flask import Blueprint

# from src.app import db

rest = Blueprint('src', __name__)

@rest.route('/', methods=['GET'])
def hello():

    return 'Hello World!'

@rest.route('/test', methods=['GET'])
def test():

    return "Testing"
    