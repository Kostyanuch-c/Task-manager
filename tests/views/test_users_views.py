from http import HTTPStatus

from django.http import Http404
from django.shortcuts import reverse

import pytest
from tests.factories.users import UserModelFactory
from tests.fixtures.forms.users import users_form_data  # noqa
from tests.fixtures.login_decorator import login_user
from tests.fixtures.services.users import (  # noqa
    user_create_data,
    user_service,
)

from task_manager.users.entities import UserInputEntity
from task_manager.users.services.user_service import UserService


def test_index(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert "Task Manager — это удобный инструмент для управления задачами." in response.content.decode('utf-8')


@login_user
@pytest.mark.django_db
def test_index_after_authorized(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert "Добро пожаловать в Task Manager!" in response.content.decode(
        "utf-8",
    )


@pytest.mark.django_db
def test_list_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_list_users_after_authorized(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
):
    password = user_create_data.password
    fetched_user = user_service.create_object(user_create_data)

    client.login(username=fetched_user.username, password=password)
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert fetched_user.username in response.content.decode("utf-8")


@pytest.mark.django_db
def test_update_user_without_login(client):
    expected_count = 5
    UserModelFactory.create_batch(expected_count)
    response = client.get("/users/5/update/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


@pytest.mark.django_db
def test_update_user_with_login(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
        users_form_data: dict,
):
    password = user_create_data.password
    fetched_user = user_service.create_object(user_create_data)

    client.login(username=fetched_user.username, password=password)

    response = client.post(
        reverse("update_user", args=[fetched_user.id]),
        data=users_form_data,
    )

    assert response.status_code == HTTPStatus.FOUND, f"{fetched_user.username=}"
    assert response.url.startswith(reverse("users_list"))

    user_after_update = user_service.get_object(fetched_user.id)
    assert user_after_update.username == users_form_data["username"]


@pytest.mark.django_db
def test_update_without_permission(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
):
    password = user_create_data.password
    user1 = user_service.create_object(user_create_data)
    user2 = UserModelFactory.create()

    client.login(username=user1.username, password=password)
    response = client.get(reverse("update_user", args=[user2.id]))

    assert response.status_code == HTTPStatus.FOUND

    url = reverse("users_list")
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_delete_user_without_login(client):
    expected_count = 5
    UserModelFactory.create_batch(expected_count)
    response = client.get("/users/5/delete/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


@pytest.mark.django_db
def test_delete_user_with_login(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
):
    password = user_create_data.password
    fetched_user = user_service.create_object(user_create_data)

    client.login(username=fetched_user.username, password=password)

    response = client.post(
        reverse("delete_user", args=[fetched_user.id]),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("users_list"))

    with pytest.raises(Http404):
        user_service.get_object(fetched_user.id)


@pytest.mark.django_db
def test_delete_without_permission(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
):
    password = user_create_data.password
    user1 = user_service.create_object(user_create_data)
    user_2 = UserModelFactory.create()

    client.login(username=user1.username, password=password)
    response = client.get(reverse("delete_user", args=[user_2.id]))

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("users_list")
    assert response.url.startswith(login_url)


@pytest.mark.django_db
def test_registration_user(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
        users_form_data: dict,
):
    response = client.post(reverse("create_user"), data=users_form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("login"))

    users = user_service.get_all_objects()
    assert len(users) == 1


def test_users_update_without_login_and_without_users(client):
    response = client.get("users/1/update/")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "Здесь нет того, что вы ищете" in response.content.decode("utf-8")


def test_users_delete_without_login_and_without_users(client):
    response = client.get("users/1/delete/")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "Здесь нет того, что вы ищете" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_login(
        client,
        user_service: UserService,
        user_create_data: UserInputEntity,
):
    password = user_create_data.password
    fetched_user = user_service.create_object(user_create_data)
    response = client.post(reverse('login'), data={'username': fetched_user.username, 'password': password})

    assert response.status_code == HTTPStatus.FOUND
    url = reverse("index")
    assert response.url.startswith(url)
    assert response.wsgi_request.user.is_authenticated


@login_user
@pytest.mark.django_db
def test_logout(client):
    response = client.post(reverse('logout'))

    assert response.status_code == HTTPStatus.FOUND
    url = reverse("index")
    assert response.url.startswith(url)
    assert not response.wsgi_request.user.is_authenticated
