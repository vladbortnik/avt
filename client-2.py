import requests


user = {'name': 'Marley', 'age': 36}

key = '123'

response = requests.post('http://localhost:5000',
                         json={'user': user, 'key': key})

print(response.json(), response.status_code)
