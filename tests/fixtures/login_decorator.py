import functools

from task_manager.users.entities import UserInputEntity
from task_manager.users.services.user_service import UserService


USER_SERVICE = UserService()
USER_CREATE_DATA = UserInputEntity(
    first_name="New first_name",
    last_name="New last_name",
    username="new_username",
    password="new12345612dsds",
)


def login_user(func):
    @functools.wraps(func)
    def inner(client, *args, **kwargs):
        password = USER_CREATE_DATA.password
        user = USER_SERVICE.create_object(USER_CREATE_DATA)
        client.login(username=user.username, password=password)
        return func(client, *args, **kwargs)

    return inner

#
# def login_user(cl):
#     def wrapper(func):
#         @functools.wraps(func)
#         def inner(*args, **kwargs):
#             user = USER_SERVICE.create_object(USER_CREATE_DATA)
#             cl.login(username=user.username, password=user.password)
#             return func(*args, **kwargs)
#
#         return inner
#
#     return wrapper
