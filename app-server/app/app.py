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
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from os import environ
from sqlalchemy.ext.declarative import declarative_base
from flask import jsonify


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

engine = create_engine(f"postgresql://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}@{environ.get('POSTGRES_HOST')}/{environ.get('POSTGRES_DB')}")

Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), default=None, unique=False)
    age = Column(Integer, default=None)

    def to_dict(self):

        return {'user_id': self.id, 'user_name': self.name, 'user_age': self.age}


@app.route('/create_table', methods=['GET'])
def create_table():
    User.__table__.create(engine)

    return jsonify(engine.table_names())


@app.route('/table_drop', methods=['GET'])
def table_drop():
    User.__table__.drop(engine)

    return jsonify(engine.table_names())


@app.route('/table_list', methods=['GET'])
def table_list():

    # return jsonify(engine.table_names())
    return {'table_names': engine.table_names()}


@app.route('/user', methods=['POST'])
def user_create():
    if not request.is_json:
        return {'error': 'request is not json'}, 422

    try:
        user = request.get_json()['user']
    except KeyError:
        return {'error': 'no user in request'}, 422

    with session_scope() as session:
        user = User()
        user.name = VALID_USER['name']
        user.age = VALID_USER['age']
        session.add(user)

    return {'user_id': user.id}, 201


# @app.route('/user', methods=['POST'])
# def create_user():
#     if not request.is_json:
#         return {'error': 'request is not json'}, 422

#     try:
#         user = request.get_json()['user']
#     except KeyError:
#         return {'error': 'no user in request'}, 422

#     user_id = storage.create(user)

#     return {'user_id': user_id}, 201

@app.route('/user/<user_id>', methods=['GET'])
def user_read(user_id):
    with session_scope() as session:
        user = session.query(User).get(user_id)

    return {'user': user.to_dict()}, 200

# http://localhost/user/<user_id>
# http://localhost/user/1
# @app.route('/user/<user_id>', methods=['GET'])
# def user_read(user_id):

#     user = storage.read(user_id)

#     return {'user': user}, 200


@app.route('/user/<user_id>', methods=['PATCH'])
def user_update(user_id):
    if not request.is_json:
        return {'error': 'request is not json'}, 422

    try:
        user = request.get_json()['user']
    except KeyError:
        return {'error': 'no user in request'}, 422

    try:
        user = request.get_json()['user']
    except KeyError:
        return {'error': 'no user in request'}, 422

    try:
        new_name = user['name']
    except KeyError:
        return {'error': "user['name'] error"}, 422

    try:
        new_age = user['age']
    except KeyError:
        return {'error': "user['age'] error"}, 422

    with session_scope() as session:
        user = session.query(User).get(user_id)
        user.name = new_name
        user.age = new_age

    return {'new_user': user.to_dict()}, 200


# @app.route('/user/<user_id>', methods=['PATCH'])
# def user_update(user_id):
#     if not request.is_json:
#         return {'error': 'request is not json'}, 422

#     # Easier to ask for forgiveness than permission: EAFP
#     # If not request.get_json()['user'] then ...
#     try:
#         user = request.get_json()['user']
#     except KeyError:
#         return {'error': 'no user in request'}, 422

#     try:
#         name = user['name']
#     except KeyError:
#         return {'error': "user['name'] error"}, 422

#     try:
#         age = user['age']
#     except KeyError:
#         return {'error': "user['age'] error"}, 422

#     user_id = storage.update(user_id, user)

#     if user_id:
#         return {'user_id': user_id}, 200
#     else:
#         return {'error': 'user not found'}, 404


@app.route('/user/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    with session_scope() as session:
        user = session.query(User).get(user_id)

        if user:
            user_id = user.id
            session.delete(user)
            return {'user_id': user_id}, 200
        else:
            return {'error': 'user not found'}, 404


# @app.route('/user/<user_id>', methods=['DELETE'])
# def user_delete(user_id):

#     user_id = storage.delete(user_id)

#     if user_id:
#         return {'user_id': user_id}, 200
#     else:
#         return {'error': 'user not found'}, 404


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

    # token = jwt.encode(VALID_USER, app.config['SECRET_KEY'])
    token = jwt.encode(VALID_USER, app.config['SECRET_KEY']).decode('utf-8')

    print(token)

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
