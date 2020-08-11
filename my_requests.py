import requests
import json

response = requests.get('http://localhost:5000')

print(response.text, response.status_code)

response = requests.post('http://localhost:5000/user')

print(response.text, response.status_code)

user = {'name': 'Bob', 'age': '36'}

response = requests.post('http://localhost:5000/user', data=user)

print(response.text, response.status_code)
