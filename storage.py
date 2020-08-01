import json
from uuid import uuid4

class Storage:
	def __init__(self, filename):
		self.filename = filename

	#create, read, update, delete

	# class Pair:
	# 	def __init__(self, k, v):
	# 		self.k = id
	# 		self.v = user[user_id]

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
			if json.loads(line)['id'] == user_id:
				file_object.close()
				return json.loads(line)
		file_object.close()
		return -1

	def update(self, user, user_id):
		file_object = open(self.filename, 'w+')
		for line in file_object.readlines():
			if json.loads(line)['id'] == user_id:

				# --- CONTINUE HERE  ------
				#json.dumps(user.add(user_id))
				#json.loads(line)['id'].name = user.name
				file_object.close()
				return user_id
		file_object.close()
		return -1


storage = Storage('user.txt')
storage.create({'name': 'Bob', 'age': '26'})
id = storage.create({'name': 'Marley', 'age': '28'})
print(storage.read(id))
storage.update({'name': 'Bob', 'age': '50'}, id)
print(storage.read(id))

#print(id)

#print(read('667db193-12da-4f06-8514-71875791e15d'))
