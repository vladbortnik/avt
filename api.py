from storage import Storage
from pprint import pprint

class API:
	def __init__(self, storage, key):
		self.storage = storage
		self.key = key

	def decorator(function):
		def wrapper(self, *args, **kwargs):
			if self.key != kwargs['key']:
				return 403
			return function(self, *args, **kwargs)
		return wrapper


	@decorator
	def post(self, user, key):
		return self.storage.create(user)

	@decorator
	def get(self, user_id, key):
		return self.storage.read(user_id)

	@decorator
	def update(self, user_id, user, key):
		return self.storage.update(user_id, user)

	@decorator
	def delete(self, user_id, key):
		return self.storage.delete(user_id)


# TEMPLATE: HOW TO PASS UNKNOWN ARGUMENTS TO THE DECORATOR
# function(*args, **kwargs)



# def decorator(function):
#     def wrapper(value):
#         print('start')
#         function(value)
#         print('end')
#     return wrapper


# @decorator
# def function(value):
#     print(value)

# # function = decorator(function)
# function('test')