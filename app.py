from flask import Flask

app = Flask(__name__)


@app.route('/')
def get():
    return 'YOO'


@app.route('/user', methods=['POST'])
def post():
    return 'POST Request Succesfull'
