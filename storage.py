import json
from uuid import uuid4
import sys
import fileinput

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
			cur_user = json.loads(str(line))
			if cur_user['id'] == user_id:
				file_object.close()
				return cur_user
		file_object.close()
		return {-1: -1}

	# def file_update(self, user_id, user):
	# 	#file_object = open(self.filename, 'r+')
	# 	for line in fileinput.input(self.filename, inplace=1):
	# 		cur_user = json.loads(line)
	# 		if cur_user['id'] == user_id:
	# 			cur_user['age'] = user['age']
	# 			cur_user['id'] = user_id
	# 			#user.update('age': '36')
	# 			#user.update('id': user_id)
	# 			json_data = json.dumps(cur_user)
	# 			#new_line = line.replace(line, json_data)
	# 			sys.stdout.write(json_data)
	# 			print('ok!')
	# 			#  ---- CONTINUE HERE ------

				
				
	# 			#file_object.write(json_data + '\n')
	# 			#file_object.close()
	# 			return user_id
	# 	#file_object.close()
	# 	return -1

	def file_update(self, user_id, user):
		with fileinput.input(self.filename, inplace=True) as f:
			for line in f:
				if line.consist(str(user_id)):
					new_line = '123'
					new_line = line.replace(line, new_line)
					print(new_line, end='')
		return -1



storage = Storage('user.txt')
id1 = storage.create({'name': 'Bob', 'age': '26'})
id2 = storage.create({'name': 'Marley', 'age': '28'})
print(storage.read(id1))
print(storage.read(id2))
storage.file_update(id2, {'name': 'Bob', 'age': '36'})
print(storage.read(id2))

#print(id)

#print(read('667db193-12da-4f06-8514-71875791e15d'))
