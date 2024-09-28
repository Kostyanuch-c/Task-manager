import functools

from tests.factories.users import UserModelFactory


USER_PASSWORD = "new12345612dsds"


def login_and_return_user(func):
    @functools.wraps(func)
    def inner(client, *args, **kwargs):
        password = USER_PASSWORD
        user = UserModelFactory.create(
            first_name="New first_name",
            last_name="New last_name",
            username="new_username",
            password=password,
        )

        client.login(username=user.username, password=password)
        kwargs['login_user'] = user
        return func(client, *args, **kwargs)

    return inner


def login_user(func):
    @functools.wraps(func)
    def inner(client, *args, **kwargs):
        password = USER_PASSWORD
        user = UserModelFactory.create(
            first_name="New first_name",
            last_name="New last_name",
            username="new_username",
            password=password,
        )

        client.login(username=user.username, password=password)
        return func(client, *args, **kwargs)

    return inner
