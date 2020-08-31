import json
from uuid import uuid4
from rich.console import Console
import os.path

console = Console()


class Storage:
    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return f'<Storage filename={self.filename}>'

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
        # list(filter(is_not_user, users))

        # TODO: Why they are always equal??
        # if users == filtered_list:
        #     return False

        with open(self.filename, 'w') as file_object:
            for user in filtered_list:
            # for user in users:
                file_object.write(json.dumps(user) + '\n')

        return user_id

    def list_all(self):
        users = []
        if not os.path.isfile(self.filename):
            return users
        with open(self.filename, 'r') as file_object:
            for line in file_object.readlines():
                users.append(line)
                console.log(f'line: {line}', log_locals=True)
        return users
