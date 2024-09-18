from django.http import Http404

import pytest
from tests.factories.users import UserModelFactory
from tests.fixtures.services.users import (  # noqa
    user_create_data,
    user_service,
)

from task_manager.users.entities import UserInputEntity
from task_manager.users.exceptions import UsernameIsNotFreeException
from task_manager.users.services.user_service import UserService


@pytest.mark.django_db
def test_get_users_all(user_service: UserService):
    expected_count = 5
    users = UserModelFactory.create_batch(expected_count)
    usernames = {user.username for user in users}

    fetched_users = user_service.get_all_objects()
    fetched_usernames = {user.username for user in fetched_users}
    assert len(fetched_users) == expected_count
    assert usernames == fetched_usernames


@pytest.mark.django_db
def test_get_users_zero(user_service: UserService):
    fetched_users = user_service.get_all_objects()
    assert len(fetched_users) == 0, f"{fetched_users=}"


@pytest.mark.django_db
def test_create_user(
    user_service: UserService,
    user_create_data: UserInputEntity,
):
    fetched_user = user_service.create_object(user_create_data)

    assert fetched_user is not None, f"{fetched_user=}"
    assert (
        fetched_user.full_name
        == f"{user_create_data.first_name} {user_create_data.last_name}"
    )
    assert fetched_user.username == user_create_data.username
    assert fetched_user.password == user_create_data.password


@pytest.mark.django_db
def test_create_user_username_already_exists(
    user_service: UserService,
    user_create_data: UserInputEntity,
):
    UserModelFactory.create(
        first_name="New first_name",
        last_name="New last_name",
        username="new_username",
        password="new12345612dsds",
    )
    with pytest.raises(UsernameIsNotFreeException):
        user_service.create_object(user_create_data)


@pytest.mark.django_db
def test_update_user_correct(
    user_service: UserService,
    user_create_data: UserInputEntity,
):
    user = UserModelFactory.create()

    user_service.update_object(user_id=user.id, user_data=user_create_data)

    fetched_user = user_service.get_object(user.id)

    assert (
        fetched_user.full_name
        == f"{user_create_data.first_name} {user_create_data.last_name}"
    )
    assert fetched_user.username == user_create_data.username
    assert fetched_user.password == user_create_data.password
    assert fetched_user.created_at == user.date_joined
    assert fetched_user.id == user.id


@pytest.mark.django_db
def test_update_user_username_already_exists(
    user_service: UserService,
    user_create_data: UserInputEntity,
):
    user = UserModelFactory.create(
        first_name="New first_name",
        last_name="New last_name",
        username="new_username",
        password="new12345612dsds",
    )
    with pytest.raises(UsernameIsNotFreeException):
        user_service.update_object(user_id=user.id, user_data=user_create_data)


@pytest.mark.django_db
def test_delete_user(user_service: UserService):
    user = UserModelFactory.create()

    user_service.delete_object(user.id)

    with pytest.raises(Http404):
        user_service.get_object(user.id)
