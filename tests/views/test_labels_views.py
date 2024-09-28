from http import HTTPStatus

from django.http import Http404
from django.shortcuts import (
    get_object_or_404,
    reverse,
)

import pytest
from tests.factories.labels import LabelModelFactory
from tests.fixtures.forms.labels import label_form_data  # noqa: F401
from tests.fixtures.login_decorator import login_user

from task_manager.tasks.models import Label


def test_get_labels_without_login(client):
    response = client.get("/labels/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


def test_get_labels_create_without_login(client):
    response = client.get("/labels/create/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


def test_label_update_without_login_and_without_statuses(client):
    response = client.get("labels/1/update/")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "Здесь нет того, что вы ищете" in response.content.decode("utf-8")


def test_label_delete_without_login_and_without_statuses(client):
    response = client.get("labels/1/delete/")
    assert response.status_code == HTTPStatus.NOT_FOUND


@login_user
@pytest.mark.django_db
def test_list_label(
        client,
):
    label = LabelModelFactory.create()
    response = client.get("/labels/")

    assert response.status_code == HTTPStatus.OK
    assert label.name in response.content.decode("utf-8")


@login_user
@pytest.mark.django_db
def test_create_label(
        client,
        label_form_data: dict,  # noqa: F811
):
    response = client.post(reverse("label_create"), data=label_form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("label_list"))

    labels = Label.objects.all()
    assert len(labels) == 1


@login_user
@pytest.mark.django_db
def test_label_update_with_login(
        client,
        label_form_data: dict,  # noqa: F811
):
    label = LabelModelFactory.create()
    response = client.post(
        reverse("label_update", args=[label.id]),
        data=label_form_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("label_list"))

    label_after_update = Label.objects.get(id=label.id)
    assert label_after_update.name == label_form_data["name"]


@login_user
@pytest.mark.django_db
def test_label_delete_with_login(
        client,
):
    label = LabelModelFactory.create()
    response = client.post(
        reverse("label_delete", args=[label.id]),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("label_list")), f"{response.url}"

    with pytest.raises(Http404):
        get_object_or_404(Label, pk=label.id)
