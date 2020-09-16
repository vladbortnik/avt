from flask import Flask, render_template
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
def read_user(user_id):

    user_id = request.args[';user_id']
    user = storage.read_user(user_id)

    return {'user': user}, 200


    # if not request.is_json:
    #     return {'error': 'request is not json'}, 422
    # try:
    #     pass

    # except KeyError:
    #     return {f'error': 'no user_id in request'}, 422

    # user = storage.read(user_id)

    # return {f'user': user}, 200


# # FAET: HANDLING POST REQUEST via JSON
# @app.route('/register', methods=['GET', 'POST'])
# def post():
#     if request.method == 'POST':

#         # console.log('oookkkkkk')

#         response = request.data


#         # TODO: CONTINUE HERE.
#         # MAKE SURE THIS FUNCTIONS IS LEGIT.
#         if response.is_json() is False:
#             print(response)
#         else:
#             data = request.get_json()

#         # is_json(mimetype)  # noqa: F821


#         console.log(f'data = {data}', log_locals=True)

#         # console.log(f'data = {data}', log_locals=True)
#         # user = json.loads(response.data)
#         # key = response.json().key

#         user = {'name': data['name'], 'age': data['age']}
#         key = data['key']

#         user_id = api.post(user, key=key)

#         if user_id != str(403):

#             # PROBLEM IS THAT 'render_template' RETURNS OLD-SCHOOL 'WEB FORM'
#             # HOWEVER THE TREND TODAY IS TOWARDS
#             return render_template('index.html', result='Success!',
#                                    name=user['name'], age=user['age'], user_id=user_id)  # noqa: E501

#         return render_template('index.html', result='Authorization Fail! Wrong key!')  # noqa: E501

#     return render_template('register-2.html')


# FAET: HANDLING POST REQUEST via HTML Form
# @app.route('/register', methods=['GET', 'POST'])
# def post():
#     if request.method == 'POST':

#         data = request.form

#         console.log(f'data = {data}', log_locals=True)

#         user = {'name': data['name'], 'age': data['age']}
#         key = data['key']

#         user_id = api.post(user, key=key)

#         if user_id != str(403):
#             return render_template('index.html', result='Success!',
#                                    name=user['name'], age=user['age'], user_id=user_id)  # noqa: E501

#         return render_template('index.html', result='Authorization Fail! Wrong key!')  # noqa: E501

#     return render_template('register.html')


@app.route('/find-user', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':

        data = request.form

        user_id = data['user_id']
        key = data['key']
        user = api.get(user_id, key=key)

        if user == 403:
            return render_template('index.html', result='Authorization Fail! Wrong key!')  # noqa: E501
        elif not bool(user):
            return render_template('index.html', result='User not found.')

        console.log(f'user: {user}', log_locals=True)

        name = user['name']
        age = user['age']

        return render_template('index.html', result='User Found!!!',
        name=name, age=age, user_id=user_id)  # noqa: E128

    return render_template('find-user.html')


@app.route('/list-all-users', methods=['GET', 'POST'])
def list_all():
    if request.method == 'POST':
        key = request.form['key']

        users = api.list_all(key=key)

        if users == 403:
            return render_template('index.html', result='Authorization Fail! Wrong key!')
        if not bool(users):
            return render_template('index.html', result='List of Users is empty!')
        else:
            return render_template('list-users.html', result='Here is the list of Users: ', users=users)

    return render_template('get-list-users.html', key='key')


@app.route('/delete-user', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        key = request.form['key']
        user_id = request.form['user_id']

        users = api.delete(user_id, key=key)

        if users == 403:
            return render_template('index.html', result='Authorization Fail! Wrong key!')
        elif not bool(users):
            return render_template('index.html', result='There is no such a user.')

        return render_template('index.html', result=f'Success! User: {user_id} - is deleted.')

    return render_template('delete-user-form.html')


@app.route('/update-user', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = request.form
        key = data['key']
        user_id = data['user_id']
        new_user = {'name': data['name'], 'age': data['age']}

        user_id = api.update(user_id, new_user, key=key)

        if user_id == 403:
            return render_template('index.html', result='Authorization Fail! Wrong key!')
        if user_id is None:
            return render_template('index.html', result='There is no such a user.')

        return render_template('index.html', result=f'Success! User: {user_id} - is updated!',
                               name=new_user['name'], age=new_user['age'],
                               user_id=user_id)

    return render_template('update-user-form.html')


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
