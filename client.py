import requests
import json


response = requests.get('http://localhost:5000')

print(response.text, response.status_code)

response = requests.post('http://localhost:5000/user')

print(response.text, response.status_code)

user = {'name': 'Bob', 'age': '36'}
# GOES AS 'FORM' --  this way:
#
# response = requests.post('http://localhost:5000/user', data=user)
#
#  $ form = request.form
#  $  console.log(f'POST', log_locals=True)

# Variant 2
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#accessing-request-data
#
# response = requests.post('http://localhost:5000/user',
#                         data={'user': json.dumps(user)})

response = requests.post('http://localhost:5000/user',
                         json={'user': user, 'user_2': user})

print(response.json(), response.status_code)
