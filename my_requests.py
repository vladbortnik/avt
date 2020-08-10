import requests

response = requests.get('http://localhost:5000')

print(response.text, response.status_code)

response = requests.post('http://localhost/user:5000')

print(response.text, response.status_code)
