from http import HTTPStatus

from django.http import Http404
from django.shortcuts import reverse

import pytest
from tests.factories.labels import LabelModelFactory
from tests.fixtures.forms.labels import label_form_data
from tests.fixtures.login_decorator import login_user
from tests.fixtures.services.labels import label_service

from task_manager.tasks.services.label_service import LabelService


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
        label_service: LabelService,
        label_form_data: dict,
):
    response = client.post(reverse("label_create"), data=label_form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("label_list"))

    labels = label_service.get_all_objects()
    assert len(labels) == 1


@login_user
@pytest.mark.django_db
def test_label_update_with_login(
        client,
        label_service: LabelService,
        label_form_data: dict,
):
    label = LabelModelFactory.create()
    response = client.post(
        reverse("label_update", args=[label.id]),
        data=label_form_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("label_list"))

    label_after_update = label_service.get_object(label.id)
    assert label_after_update.name == label_form_data["name"]


@login_user
@pytest.mark.django_db
def test_label_delete_with_login(
        client,
        label_service: LabelService,
):
    label = LabelModelFactory.create()
    response = client.post(
        reverse("label_delete", args=[label.id]),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("label_list")), f"{response.url}"

    with pytest.raises(Http404):
        label_service.get_object(label.id)
