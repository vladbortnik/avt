from storage import Storage
from api import API
from pprint import pprint


storage = Storage('user.txt')
api = API(storage=storage,
          key='123')

key = '123'

# CREATE
user = {'name': 'bob marley',
        'age': 26}
user_id = api.post(user, key=key)

pprint(user)
pprint(user_id)

# READ
user = api.get(user_id, key=key)

pprint(user)

# UPDATE
user = {'name': 'Bob Marley',
        'age': 26}
user_id = api.update(user_id, user, key=key)

pprint(user)
pprint(user_id)

# DELETE
user_id = api.delete(user_id, key=key)

pprint(user_id)
