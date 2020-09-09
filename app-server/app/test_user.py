import requests
# import pytest
# import os
from uuid import UUID
from rich.console import Console


console = Console()


name = ''
age = 0
user_id = None


def test_create_user():
    user = {'name': 'Steve-0', 'age': 3}
    # REQUESTs will change dict {'user': user} to JSON
    response = requests.post('http://localhost:5000/user', json={'user': user})

    assert response.status_code == 201

    # os.remove('user.txt')


def test_create_user_not_json():
    user = {'name': 'Steve-1', 'age': 13}
    response = requests.post('http://localhost:5000/user', data={'user': user})

    assert response.status_code == 422

    # os.remove('user.txt')


def test_create_user_check_uuid():
    user = {'name': 'Steve-2', 'age': 23}
    response = requests.post('http://localhost:5000/user', json={'user': user})

    user_id = response.json()['user_id']

    # console.log(f'user_id = {user_id}', log_locals=True)

    assert type(UUID(user_id)) is UUID

    # os.remove('user.txt')


# CONTINUE HERE: nethod=['GET'], 'user_id' is passed thru URL param (not json)
def test_read_user():
    # QUESTION: Is it better to just pass 'user_id' from prev func??
    # user_sent = {'name': 'Steve-3', 'age': 33}
    # response = requests.post('http://localhost:5000/user', json={'user': user_sent})
    # user_id = response.json()['user_id']

    response = requests.get('http://localhost:5000/user', params={'user_id': user_id})
    # user_received = response.json()['user']

    assert response.status_code == 200


# CONTINUE HERE: nethod=['GET'], 'user_id' is passed thru URL param (not json)
def test_read_user_check_name_n_age_correct():
    # Let's create a user for this test func()
    user_sent = {'name': 'Steve-443', 'age': 443}
    response = requests.post('http://localhost:5000/user', json={'user': user_sent})
    user_id = response.json()['user_id']

    response = requests.post('http://localhost:5000/user', json={'user_id': user_id})
    user_received = response.json()['user']

    assert user_sent['name'] is user_received['name'] and user_sent['age'] is user_received['age']


def update_user():
    pass


def list_users():
    pass


def delete():
    pass


# os.remove('user.txt')
