from flask import Flask
# from flask import render_template
from flask import request
# QUESTION: WHY Error: NO MODULE NAMED 'requests' ???
# ANSWQER: need to do: $ 'docker-compose build'
# import requests
from rich.console import Console
# from api import API
from storage import Storage
import logging
from rich.logging import RichHandler
import jwt

VALID_USER = {'name': 'Steve-77', 'age': 66}


app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc3c9cc6-6748-49f3-b5eb-1eb711a7d0de'

#########################################

# Simple Python logging

# logger.addHandler(handler)  # attach the handler to the app's logger

#########################################

# import requests
# from uuid import UUID
# from pprint import pprint
# from rich.logging import RichHandler
# import logging
# import json
# from flask import jsonify
# from sys import argv
# from flask import redirect

#########################################

# Rich logging ( - is better than Python Logging)

logging.basicConfig(level="NOTSET",
                    format="%(message)s",
                    datefmt="[%X]",
                    handlers=[RichHandler()])  # noqa: F821
log = logging.getLogger("rich")
logging.getLogger("requests").setLevel(logging.WARNING)
log.info('Logger is enabled')

#########################################

console = Console()


storage = Storage('user.txt')
# api = API(storage, key='123')


# @app.route('/')
# def index():
#     return render_template('index.html', result='', user='', name='', age='', user_id='')


@app.route('/user', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'request is not json'}, 422

    try:
        user = request.get_json()['user']
    except KeyError:
        return {'error': 'no user in request'}, 422

    user_id = storage.create(user)

    return {'user_id': user_id}, 201


# http://localhost/user/<user_id>
# http://localhost/user/1
@app.route('/user/<user_id>', methods=['GET'])
def user_read(user_id):

    user = storage.read(user_id)

    return {'user': user}, 200


@app.route('/user/<user_id>', methods=['PATCH'])
def user_update(user_id):
    if not request.is_json:
        return {'error': 'request is not json'}, 422

    # Easier to ask for forgiveness than permission: EAFP
    # If not request.get_json()['user'] then ...
    try:
        user = request.get_json()['user']
    except KeyError:
        return {'error': 'no user in request'}, 422

    try:
        name = user['name']
    except KeyError:
        return {'error': "user['name'] error"}, 422

    try:
        age = user['age']
    except KeyError:
        return {'error': "user['age'] error"}, 422

    user_id = storage.update(user_id, user)

    if user_id:
        return {'user_id': user_id}, 200
    else:
        return {'error': 'user not found'}, 404


@app.route('/user/<user_id>', methods=['DELETE'])
def user_delete(user_id):

    user_id = storage.delete(user_id)

    if user_id:
        return {'user_id': user_id}, 200
    else:
        return {'error': 'user not found'}, 404


@app.route('/user_authenticate', methods=['POST'])
def user_authenticate():
    # Receive login & password
    try:
        response = request.is_json
    except KeyError:
        return {'error': 'not a json'}

    login = request.get_json()['login']
    password = request.get_json()['password']

    # Check the correctness of the credentials

    # Assign & Send a token to the user

    token = jwt.encode(VALID_USER, app.config['SECRET_KEY'])

    return {'user': VALID_USER, 'token': token}, 200



#########################################

# @app.route('/validation-form', methods=['GET', 'POST'])
# def validation_form():
#     return render_template('validation-form.html')

#########################################


#########################################

# jsonify() returns 'request' object
# @app.route('/user', methods=['GET', 'POST'])
# def post():
    #    console.log(f'{request.args}')
#   user = request.get_json()['user']
#   console.log(f'POST', log_locals=True)
#   return jsonify({'user': user})

#########################################
