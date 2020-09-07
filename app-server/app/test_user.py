import requests
import pytest
import os
from uuid import UUID


def test_create_user():
    user = {'name': 'Steve', 'age': 33}
    # REQUEST will change dict {'user': user} to JSON
    response = requests.post('http://localhost:5000/user', json={'user': user})

    assert response.status_code == 201

    # os.remove('user.txt')


def test_create_user_not_json():
    user = {'name': 'Steve', 'age': 33}
    response = requests.post('http://localhost:5000/user', data={'user': user})

    assert response.status_code == 422

    # os.remove('user.txt')


def test_create_user_check_uuid():
    user = {'name': 'Steve', 'age': 33}
    response = requests.post('http://localhost:5000/user', json={'user': user})

    user_id = response.json()['user_id']

    assert type(user_id) is UUID

    # os.remove('user.txt')


def read_user():
    pass


def update_user():
    pass


def list_users():
    pass


def delete():
    pass


# os.remove('user.txt')
