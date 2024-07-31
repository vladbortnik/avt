import jwt
import logging
from os import environ
from flask import Flask, request, jsonify
from rich.console import Console
from rich.logging import RichHandler
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
# import OutputMixin

VALID_USER = {'name': 'Steve-77', 'age': 66}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc3c9cc6-6748-49f3-b5eb-1eb711a7d0de'

#########################################

# Simple Python logging:
# (attaches the handler to the app's logger)

# logger.addHandler(handler)

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
# storage = Storage('user.txt')

######################################################
# NO LOGIC. JUST REMEMBER: 'engine', 'Session', 'Base'.
######################################################


engine = create_engine(f"postgresql://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}@{environ.get('POSTGRES_HOST')}/{environ.get('POSTGRES_DB')}")
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


#################################################
# THE FOLLOWING MASTERPIECE IS PURE NONSENSE OF
# THE TWISTED MIND OF 'GEORGY ALEX, THE GREAT'!!!
#################################################


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


#############################################
# FOR EVERY TABLE WE CREATE A SEPARATE CLASS
#############################################


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), default=None, unique=False)
    age = Column(Integer, default=None)

    def to_dict(self):

        return {'user_id': self.id,
                'name': self.name, 'age': self.age}


#######################
# NOW LET'S CREATE API
#######################


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


@app.route('/user/<user_id>', methods=['GET'])
def user_read(user_id):
    with session_scope() as session:
        user = session.query(User).get(user_id)

    return {'user': user.to_dict()}, 200


@app.route('/user/<user_id>', methods=['PATCH'])
def user_update(user_id):
    if not request.is_json:
        return {'error': 'request is not json'}, 422

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

        if not user:
            return {'error': 'user not found'}, 404

        user.name = new_name
        user.age = new_age

    return {'new_user': user.to_dict()}, 200


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


###############################################

# THE FOLLOWING CODE WILL BE USED AS API FOR
# USER REGISTRATION, AUTHENTICATION AND
# AUTHORIZATION AUTHORIZATION

###############################################

# ... CONTINUE HERE

###############################################


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
