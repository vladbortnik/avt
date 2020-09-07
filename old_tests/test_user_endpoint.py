import requests
from uuid import UUID
import pytest


def test_create_user():
    user = {'name': 'Gloria', 'age': 36}
    key = '123'
    response = requests.post('http://localhost:5000/user',
                             json={'user': user, 'key': key})
    assert response.status_code == 201
    assert 'user_id' in response.json()
    try:
        user_id = UUID(response.json()['user_id'])
    except AttributeError:
        pytest.fail('"user_id" is of wrong type.')
    # TODO: make sure we need the following assertion
    assert type(user_id) is UUID


def test_create_user_with_wrong_key():
    user = {'name': 'Gloria', 'age': 36}
    key = '1234'
    response = requests.post('http://localhost:5000/user',
                             json={'user': user, 'key': key})

    assert response.status_code == 403
