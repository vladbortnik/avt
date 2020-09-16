from flask import Flask
# from flask import render_template
from flask import request
# QUESTION: WHY Error: NO MODULE NAMED 'requests' ???
# import requests
from rich.console import Console
# from api import API
from storage import Storage
import logging
from rich.logging import RichHandler

app = Flask(__name__)

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






# @app.route('/update-user', methods=['GET', 'POST'])
# def update():
#     if request.method == 'POST':
#         data = request.form
#         key = data['key']
#         user_id = data['user_id']
#         new_user = {'name': data['name'], 'age': data['age']}

#         user_id = api.update(user_id, new_user, key=key)

#         if user_id == 403:
#             return render_template('index.html', result='Authorization Fail! Wrong key!')
#         if user_id is None:
#             return render_template('index.html', result='There is no such a user.')

#         return render_template('index.html', result=f'Success! User: {user_id} - is updated!',
#                                name=new_user['name'], age=new_user['age'],
#                                user_id=user_id)

#     return render_template('update-user-form.html')


# @app.route('/list-all-users', methods=['GET', 'POST'])
# def list_all():
#     if request.method == 'POST':
#         key = request.form['key']

#         users = api.list_all(key=key)

#         if users == 403:
#             return render_template('index.html', result='Authorization Fail! Wrong key!')
#         if not bool(users):
#             return render_template('index.html', result='List of Users is empty!')
#         else:
#             return render_template('list-users.html', result='Here is the list of Users: ', users=users)

#     return render_template('get-list-users.html', key='key')


# @app.route('/delete-user', methods=['GET', 'POST'])
# def delete():
#     if request.method == 'POST':
#         key = request.form['key']
#         user_id = request.form['user_id']

#         users = api.delete(user_id, key=key)

#         if users == 403:
#             return render_template('index.html', result='Authorization Fail! Wrong key!')
#         elif not bool(users):
#             return render_template('index.html', result='There is no such a user.')

#         return render_template('index.html', result=f'Success! User: {user_id} - is deleted.')

#     return render_template('delete-user-form.html')


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
