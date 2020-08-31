from flask import Flask, render_template, redirect
from sys import argv
from pprint import pprint
from flask import request
from rich.console import Console
from rich.logging import RichHandler
import logging
import json
from flask import jsonify
from api import API
from storage import Storage
from uuid import UUID


# logging.basicConfig(level="NOTSET",
#                     format="%(message)s",
#                     datefmt="[%X]",
#                     handlers=[RichHandler()])
# log = logging.getLogger("rich")
# logging.getLogger("requests").setLevel(logging.WARNING)
# log.info('Logger is enabled')

console = Console()


app = Flask(__name__)

# key = '123'
storage = Storage('user.txt')
api = API(storage, key='123')


@app.route('/')
def index():
    return render_template('index.html', result='', user='', user_name='', user_age='', user_id='')


# ##########
# @app.route('/sign-up', methods=['GET', 'POST'])
# def post():

#     if request.method == 'POST':

#         data = request.form

#         print(data)

#         return render_template('index.html', result='Success!', user='', user_id='')  # noqa: E501

#     return render_template('sign-up.html')
# ################


@app.route('/register', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':

        data = request.form

        user = {'name': data['name'], 'age': data['age']}
        key = data['key']

        user_id = api.post(user, key=key)

        if user_id != str(403):
            return render_template('index.html', result='Success!',
                                   user_name=user['name'], user_age=user['age'], user_id=user_id)  # noqa: E501

        return render_template('index.html', result='Authorization Fail! Wrong key!')  # noqa: E501

    return render_template('register.html')


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
        user_name=name, user_age=age, user_id=user_id)  # noqa: E128

    return render_template('find-user.html')


@app.route('/list-all-users', methods=['GET', 'POST'])
def list_all():
    if request.method == 'POST':
        key = request.form['key']

        # console.log(f'key: {key}', log_locals=True)

        users = api.list_all(key=key)

        # console.log(f'users: {users}', log_locals=True)

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
        else:
            user_id = api.delete(user_id, key=key)
            if user_id is False:
                return render_template('index.html', result=f'Uknown error. user_id: {user_id}')
            return render_template('index.html', result=f'Success! User: {user_id} - is deleted.')

    return render_template('delete-user-form.html')

# @app.route('/validation-form', methods=['GET', 'POST'])
# def validation_form():
#     return render_template('validation-form.html')


# ############################
# jsonify() returns 'request' object
# @app.route('/user', methods=['GET', 'POST'])
# def post():
    #    console.log(f'{request.args}')
#   user = request.get_json()['user']
#   console.log(f'POST', log_locals=True)
#   return jsonify({'user': user})
# ############################
