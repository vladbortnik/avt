from storage import Storage
from api import API


def test_create(tmp_path):
    storage = Storage(tmp_path / 'user.txt')
    api = API(storage=storage,
              key='123')
    key = '123'
    user = {'name': 'bob marley',
            'age': 26}
    user_id = api.post(user, key=key)
    assert user_id != 403


def test_read():
    assert 2 == 2


def test_update():
    assert 2 == 2


def test_delete():
    assert 2 == 2
