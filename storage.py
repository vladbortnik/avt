import json
from uuid import uuid4
from pprint import pprint

class Storage:
    def __init__(self, filename):
        self.filename = filename

    def create(self, user):
        user['id'] = str(uuid4())
        file_object = open(self.filename, 'a')
        json_data = json.dumps(user)    
        file_object.write(json_data + '\n')
        file_object.close()
        return user['id']

    def read(self, user_id):
        file_object = open(self.filename, 'r')
        for line in file_object.readlines():
            cur_user = json.loads(str(line))
            if cur_user['id'] == user_id:
                file_object.close()
                return cur_user
        file_object.close()
        return False

    def update(self, user_id, user):
        with open(self.filename, 'r') as file_object:
            users = []
            for line in file_object.readlines():
                cur_user = json.loads(line)
                users.append(cur_user)

        def is_user(user):
            return user['id'] == user_id

# LIST COMPREHENTION        
# new_list = [new_element if condition else old_element for old_element in old_list]

        users = [dict(old_user, **user) 
                 if old_user['id'] == user_id
                 else old_user
                 for old_user in users]

        if not list(filter(is_user, users)):
            return None

        with open(self.filename, 'w') as file_object:
            for user in users:
                json_data = json.dumps(user)
                file_object.write(json_data + '\n')

        return user_id

    def delete(self, user_id):
        users = []
        with open(self.filename, 'r') as file_object:
            for line in file_object.readlines():
                users.append(json.loads(line))

        def is_not_user(user):
            return user['id'] != user_id
        filtered_list = list(filter(is_not_user, users))

        with open(self.filename, 'w') as file_object:
            for user in filtered_list:
                file_object.write(json.dumps(user) + '\n')

        return user_id



# storage = Storage('user.txt')
# id1 = storage.create({'name': 'Bob', 'age': '26'})
# id2 = storage.create({'name': 'Marley', 'age': '28'})
# print(storage.update(id1, {'name': 'Bob', 'age': '36'}))
# print(storage.delete(id2))