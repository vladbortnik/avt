# from rich.logging import RichHandler
from rich.console import Console
# import logging


# logging.basicConfig(level="NOTSET",
#                     format="%(message)s",
#                     datefmt="[%X]",
#                     handlers=[RichHandler()])
# log = logging.getLogger("rich")
# logging.getLogger("requests").setLevel(logging.WARNING)
# log.info('Logger is enabled')

console = Console()
console.log(f'[bold red]error_message',
            log_locals=True)

class API:
    def __init__(self, storage, key):
        self.storage = storage
        self.key = key

    def __repr__(self):
        return f'<API key={self.key} storage={self.storage}>'

    def decorator(function):
        def wrapper(self, *args, **kwargs):
            if self.key != kwargs['key']:
                return 403
            return function(self, *args, **kwargs)
        return wrapper

    @decorator
    def post(self, user, key):
        console.log(f'[bold green]method post',
                    log_locals=True)
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


# from rich.logging import RichHandler
# from rich.console import Console

# console = Console()
# logging.basicConfig(level="NOTSET",
#                     format="%(message)s",
#                     datefmt="[%X]",
#                     handlers=[RichHandler()])
# log = logging.getLogger("rich")
# logging.getLogger("requests").setLevel(logging.WARNING)
# log.info('Logger is enabled')


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