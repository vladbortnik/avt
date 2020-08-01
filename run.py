from storage import Storage
from api import API


storage = Storage('user.txt')
api = API(storage=storage,
          key='123')

# CREATE
user = {'name': 'bob marley',
        'age': 26}
user_id = api.post(user)

# READ
user = api.get(user_id)

# UPDATE
user = {'name': 'Bob Marley',
        'age': 26}
user_id = api.update(user_id, user)

# DELETE
user_id = api.delete(user_id)
