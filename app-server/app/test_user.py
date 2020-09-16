import requests
# import pytest
# import os
from uuid import UUID
from rich.console import Console

BASE_URL = 'http://localhost:5000'
VALID_USER = {'name': 'Steve-77', 'age': 66}
NOT_VALID_USER = {'name': 'not_Steve-999', 'age': 999}

console = Console()


def test_create_user():
    user = {'name': 'Steve-0', 'age': 3}
    # REQUESTs will change dict {'user': user} to JSON
    response = requests.post(f'{BASE_URL}/user', json={'user': user})

    assert response.status_code == 201

    # os.remove('user.txt')


def test_create_user_not_json():
    user = {'name': 'Steve-1', 'age': 13}
    response = requests.post(f'{BASE_URL}/user', data={'user': user})

    assert response.status_code == 422

    # os.remove('user.txt')


def test_create_user_check_uuid():
    user = {'name': 'Steve-2', 'age': 23}
    response = requests.post(f'{BASE_URL}/user', json={'user': user})

    user_id = response.json()['user_id']

    # console.log(f'user_id = {user_id}', log_locals=True)

    assert type(UUID(user_id)) is UUID

    # os.remove('user.txt')


def test_read_user_correct_name_age():
    # QUESTION: Is it better to just pass 'user_id' from prev func?? And HOW??
    # ANSWER: Better to create user again (because we do 'pytest')...
    # ...If it was a regular code then it would better  to create a class
    # ALSO See: https://stackoverflow.com/questions/49238725/chaining-tests-and-passing-an-object-from-one-test-to-another

    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})
    user_id = response.json()['user_id']

    # console.log(f'user_id = {user_id}', log_locals=True)

    response = requests.get(f'{BASE_URL}/user/{user_id}')

    # console.log(f'URL = {response.url}', log_locals=True)

    assert response.status_code == 200
    assert response.json()['user']['name'] == VALID_USER['name']
    assert response.json()['user']['age'] == VALID_USER['age']


def update_user():
    pass


def list_users():
    pass


def delete():
    pass


# os.remove('user.txt')
