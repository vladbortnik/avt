from flask import Flask
from pprint import pprint
from flask import request
from rich.console import Console
from rich.logging import RichHandler
import logging


logging.basicConfig(level="NOTSET",
                    format="%(message)s",
                    datefmt="[%X]",
                    handlers=[RichHandler()])
log = logging.getLogger("rich")
logging.getLogger("requests").setLevel(logging.WARNING)
log.info('Logger is enabled')

console = Console()


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get():
    return 'YOO'


@app.route('/user', methods=['GET', 'POST'])
def post():
    console.log(f'{request.args}')
    return f'POST Request Succesfull: '
