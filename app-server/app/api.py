from rich.console import Console
# import logging
# from rich.logging import RichHandler

#########################################

# logging.basicConfig(level="NOTSET",
#                     format="%(message)s",
#                     datefmt="[%X]",
#                     handlers=[RichHandler()])
# log = logging.getLogger("rich")
# logging.getLogger("requests").setLevel(logging.WARNING)
# log.info('Logger is enabled')

#########################################

console = Console()

#########################################

# console.log(f'[bold red]error_message',
#             log_locals=True)

#########################################


def decorator(function):
    def wrapper(self, *args, **kwargs):
        if self.key != kwargs['key']:
            return 403
        return function(self, *args, **kwargs)
    return wrapper


class API:

    def __init__(self, storage, key):
        self.storage = storage
        self.key = key

    def __repr__(self):
        console.log('[bold __repr__(api)',
                    log_locals=True)
        return f'<API key={self.key} storage={self.storage}>'

    # TODO:- - DONE: Move decorator out of API class
    # def decorator(function):
    #     def wrapper(self, *args, **kwargs):
    #         if self.key != kwargs['key']:
    #             return 403
    #         return function(self, *args, **kwargs)
    #     return wrapper

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
    def delete(self, user_id, key='key'):
        return self.storage.delete(user_id)

    @decorator
    def list_all(self, key='key'):
        return self.storage.list_all()

#########################################

# TEMPLATE: HOW TO PASS UNKNOWN ARGUMENTS TO THE DECORATOR
# function(*args, **kwargs)

#########################################

# def decorator(function):
#     def wrapper(value):
#         print('start')
#         function(value)
#         print('end')
#     return wrapper


# Example:

# @decorator
# def function(value):
#     print(value)

# # function = decorator(function)
# function('test')

#########################################
