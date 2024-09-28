from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import (
    get_object_or_404,
    reverse,
)

import pytest
from tests.factories.users import UserModelFactory
from tests.fixtures.forms.users import users_form_data  # noqa: F401
from tests.fixtures.login_decorator import login_user


def test_index(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert "Task Manager — это" in response.content.decode("utf-8")


@login_user
@pytest.mark.django_db
def test_index_after_authorized(
        client,
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
        users_form_data: dict,  # noqa: F811
):
    password = users_form_data.get("password1")
    UserModelFactory.create(password=password)

    fetched_user = get_user_model().objects.all()[0]
    client.login(username=fetched_user.username, password=password)
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert fetched_user.username in response.content.decode("utf-8")


@pytest.mark.django_db
def test_update_user_without_login(client):
    expected_count = 3
    users = UserModelFactory.create_batch(expected_count)
    response = client.get(f"/users/{users[2].id}/delete/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


@pytest.mark.django_db
def test_update_user_with_login(
        client,
        users_form_data: dict,  # noqa: F811
):
    password = 'password'
    UserModelFactory.create(password=password)

    fetched_user = get_user_model().objects.all()[0]
    client.login(username=fetched_user.username, password=password)

    response = client.post(
        reverse("update_user", args=[fetched_user.id]),
        data=users_form_data,
    )

    assert response.status_code == HTTPStatus.FOUND, f"{fetched_user.username=}"
    assert response.url.startswith(reverse("users_list"))

    user_after_update = get_user_model().objects.get(id=fetched_user.id)
    assert user_after_update.username == users_form_data["username"]


@pytest.mark.django_db
def test_update_without_permission(client):
    password = 'password'
    UserModelFactory.create(password=password)

    user1 = get_user_model().objects.all()[0]
    user2 = UserModelFactory.create()

    client.login(username=user1.username, password=password)
    response = client.get(reverse("update_user", args=[user2.id]))

    assert response.status_code == HTTPStatus.FOUND

    url = reverse("users_list")
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_delete_user_without_login(client):
    expected_count = 3
    users = UserModelFactory.create_batch(expected_count)
    response = client.get(f"/users/{users[2].id}/delete/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


@pytest.mark.django_db
def test_delete_user_with_login(
        client,
):
    password = 'password'
    UserModelFactory.create(password=password)
    fetched_user = get_user_model().objects.all()[0]
    client.login(username=fetched_user.username, password=password)

    response = client.post(
        reverse("delete_user", args=[fetched_user.id]),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("users_list"))

    with pytest.raises(Http404):
        get_object_or_404(get_user_model(), id=fetched_user.id)


@pytest.mark.django_db
def test_delete_without_permission(
        client,
):
    password = 'password'
    UserModelFactory.create(password=password)
    user1 = get_user_model().objects.all()[0]
    user_2 = UserModelFactory.create()

    client.login(username=user1.username, password=password)
    response = client.get(reverse("delete_user", args=[user_2.id]))

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("users_list")
    assert response.url.startswith(login_url)


@pytest.mark.django_db
def test_registration_user(
        client,
        users_form_data: dict,  # noqa: F811
):
    response = client.post(reverse("create_user"), data=users_form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("login"))

    users = get_user_model().objects.all()
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
):
    password = 'password'
    UserModelFactory.create(password=password)
    fetched_user = get_user_model().objects.all()[0]
    response = client.post(
        reverse("login"),
        data={"username": fetched_user.username, "password": password},
    )

    assert response.status_code == HTTPStatus.FOUND
    url = reverse("index")
    assert response.url.startswith(url)
    assert response.wsgi_request.user.is_authenticated


@login_user
@pytest.mark.django_db
def test_logout(client):
    response = client.post(reverse("logout"))

    assert response.status_code == HTTPStatus.FOUND
    url = reverse("index")
    assert response.url.startswith(url)
    assert not response.wsgi_request.user.is_authenticated
