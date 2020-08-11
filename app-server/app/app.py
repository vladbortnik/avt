from flask import Flask
from pprint import pprint
from flask import request
from rich.console import Console
from rich.logging import RichHandler
import logging
from flask import jsonify
from api import API
from storage import Storage


logging.basicConfig(level="NOTSET",
                    format="%(message)s",
                    datefmt="[%X]",
                    handlers=[RichHandler()])
log = logging.getLogger("rich")
logging.getLogger("requests").setLevel(logging.WARNING)
log.info('Logger is enabled')

console = Console()


app = Flask(__name__)

storage = Storage('user.txt')

api = API(storage, key='123')


@app.route('/', methods=['POST'])
def create_user():
    user = request.get_json()['user']
    key = request.get_json()['key']
    user_id = api.post(user, key=key)
    return jsonify({'user_id': user_id})


# @app.route('/', methods=['GET', 'POST'])
# def get():
#   return 'YOO'

# jsonify() returns 'request' object
# @app.route('/user', methods=['GET', 'POST'])
# def post():
    #    console.log(f'{request.args}')
#   user = request.get_json()['user']
#   console.log(f'POST', log_locals=True)
#   return jsonify({'user': user})
