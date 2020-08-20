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


logging.basicConfig(level="NOTSET",
                    format="%(message)s",
                    datefmt="[%X]",
                    handlers=[RichHandler()])
log = logging.getLogger("rich")
logging.getLogger("requests").setLevel(logging.WARNING)
log.info('Logger is enabled')

console = Console()


app = Flask(__name__)

# key = '123'
storage = Storage('user.txt')
api = API(storage, key='123')


# def is_the_key_correct(key):

#     console.log(f'key == api.key is {key == api.key}', log_locals=True)
#     console.log(f'key: {key}')
#     console.log(f'api.key: {api.key}')

#     if key == api.key:
#         return True
#     return False


@app.route('/')
def index():
    return render_template('index.html', result='', user='', user_id='')


# @app.route('/register', methods=['GET', 'POST'])
# def post():
#     if request.method == 'GET':
#         return render_template('register.html')
#     elif request.method == 'POST':

#         # form = request.form
#         # key = form.

#         console.log(f"request.form.get('name') is {request.form.get('name')}", log_locals=True)
#         console.log(f"request.form.get('age') is {request.form.get('age')}", log_locals=True)
#         console.log(f"request.form.get('key') is {request.form.get('key')}", log_locals=True)
#         console.log(f"request.data is {request.data}", log_locals=True)

#         key = request.form.get('key')
#         if not is_the_key_correct(key):
#             result = 'Access DENIED: Key is wrong'
#             return render_template('index.html', result=result, user='', user_id='')

#         name = request.form.get('name')
#         age = int(request.form.get('age'))
#         user = {'name': name, 'age': age}
#         user_id = api.post(user)

#         result = 'Your data submission was Successful !!!'
#         user_id = f"Your 'user_id' is: {user_id}"
#         return render_template('index.html', result=result, user='', user_id=user_id)
#     else:
#         result = 'Unexpected Error: Your data submission was Unsuccessful'
#         # console.log(f'request.form: {request.form}', log_locals=True)
#         return render_template('index.html', result=result, user='', user_id='')


# @app.route('/get', methods=['GET', 'POST'])
# def get():
#     user_id = request.form.get('user_id')
#     key = request.form.get('key')
#     if not is_the_key_correct(key):
#         result = 'Access DENIED: Key is wrong'
#         return render_template('index.html', result=result, user='', user_id='')
#     if request.method == "GET":
#         return render_template('user.html')
#     elif request.method == 'POST':
#         if api.get_user(user_id) == True:
#             user = api.get_user(user_id)
#             result = 'User is found !!!'
#             return render_template('index.html', result=result, user=user)
#         else:
#             result = 'We were unable to find the User'
#             return render_template('index.html', result=result, user='', user_id='')


# ##########
# @app.route('/sign-up', methods=['GET', 'POST'])
# def post():

#     if request.method == 'POST':

#         data = request.form

#         print(data)

#         return render_template('index.html', result='Success!', user='', user_id='')

#     return render_template('sign-up.html')
# ################


@app.route('/register', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':

        data = request.form

        user = {'name': data['name'], 'age': data['age']}
        key = data['key']

        console.log(type(key), log_locals=True)

        user_id = api.post(user, key=key)

        console.log(user_id, log_locals=True)
        console.log(f'type(user_id) == UUID: {type(user_id) == UUID}')
        console.log(data['key'])
        console.log(f'user_id != 403: {user_id != 403}')
        if user_id != str(403):
            return render_template('index.html', result='Authorization Fail! Wrong key!', user='', user_id='')
        # elif type(user_id) == UUID:
        #     return render_template('index.html', result='Success-2!', user='', user_id=user_id)
        else:
            return render_template('index.html', result='Success-2!', user='', user_id=user_id)

    return render_template('register.html')


# @app.route('/register', method=['POST'])
# def register():
#     json_data = json.loads(request.form)
#     key = json_data['key']
#     if not is_the_key_correct(key):
#         return render_template('Authorization Failed')





# def decorator(function):
#     def wraper(self, *args, **kwargs):
#         if


# @app.route('/', methods=['POST'])
# def create_user():
#     user = request.get_json()['user']
#     key = request.get_json()['key']
#     user_id = api.post(user, key=key)
#     return {'user_id': user_id}, 201


# @app.route('/user/<id>', methods=['GET'])
# def read_user(id):
#     try:
#         decorator(api.get)
#         return {'user': user}
#     except Exception as e:
#         raise e
#     else:
#         pass
#     id =
#     user = api.get(id, key=key)



# jsonify() returns 'request' object
# @app.route('/user', methods=['GET', 'POST'])
# def post():
    #    console.log(f'{request.args}')
#   user = request.get_json()['user']
#   console.log(f'POST', log_locals=True)
#   return jsonify({'user': user})

