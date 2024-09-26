from http import HTTPStatus

from django.http import Http404
from django.shortcuts import reverse

import pytest
from tests.factories.labels import LabelModelFactory
from tests.factories.tasks import TaskModelFactory
from tests.fixtures.forms.tasks import task_form_data  # noqa: F401
from tests.fixtures.login_decorator import (
    login_and_return_user,
    login_user,
)
from tests.fixtures.services.tasks import task_service  # noqa: F401

from task_manager.tasks.services.task_service import TaskService


def test_get_tasks_without_login(client):
    response = client.get("/tasks/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


def test_get_tasks_create_without_login(client):
    response = client.get("/tasks/create/")

    assert response.status_code == HTTPStatus.FOUND

    login_url = reverse("login")
    assert response.url.startswith(login_url)


def test_tasks_update_without_login_and_without_tasks(client):
    response = client.get("tasks/1/update/")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "Здесь нет того, что вы ищете" in response.content.decode("utf-8")


def test_tasks_delete_without_login_and_without_tasks(client):
    response = client.get("statuses/1/delete/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_tasks_detail_without_login_and_without_tasks(client):
    response = client.get("tasks/1/")
    assert response.status_code == HTTPStatus.NOT_FOUND


@login_user
@pytest.mark.django_db
def test_list_task(
        client,
        task_service: TaskService,  # noqa: F811
):
    task = TaskModelFactory.create()
    response = client.get("/tasks/")

    assert response.status_code == HTTPStatus.OK
    assert task.name in response.content.decode("utf-8")


@login_user
@pytest.mark.django_db
def test_detail_task(
        client,
        task_service: TaskService,  # noqa: F811
):
    labels = [LabelModelFactory.create(name="test")]
    task = TaskModelFactory.create(labels=labels)
    response = client.get(reverse("task_detail", args=[task.id]))

    assert response.status_code == HTTPStatus.OK
    assert task.name in response.content.decode("utf-8")
    assert task.author.full_name in response.content.decode("utf-8")
    assert 'test' in response.content.decode("utf-8")


@login_and_return_user
@pytest.mark.django_db
def test_create_task(client, task_service: TaskService, task_form_data: dict, **kwargs):  # noqa
    current_user = kwargs['login_user']

    response = client.post(reverse("task_create"), data=task_form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("task_list"))

    task = task_service.get_all_objects()[0]
    assert task.name == task_form_data['name']
    assert task_form_data['description'] == task_form_data['description']
    assert task.author == current_user
    assert task.status.id == task_form_data['status']
    assert task.executor.id == task_form_data['executor']
    assert {label.id for label in task.labels.all()} == set(task_form_data['labels'])


@login_and_return_user
@pytest.mark.django_db
def test_update_task(
        client,
        task_service: TaskService,  # noqa: F811
        task_form_data: dict,  # noqa: F811
        **kwargs,
):
    current_user = kwargs['login_user']

    task = TaskModelFactory.create()

    response = client.post(
        reverse("task_update", args=[task.id]),
        data=task_form_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("task_list"))

    task_after_update = task_service.get_object(task.id)
    assert task_after_update.name == task_form_data['name']
    assert task_after_update.description == task_form_data['description']
    assert task_after_update.author == current_user
    assert task_after_update.status.id == task_form_data['status']
    assert task_after_update.executor.id == task_form_data['executor']
    assert {label.id for label in task_after_update.labels.all()} == set(task_form_data['labels'])


@login_user
@pytest.mark.django_db
def test_task_delete_with_login_without_permission(client, task_service: TaskService):  # noqa: F811
    task = TaskModelFactory.create()

    response = client.post(
        reverse("task_delete", args=[task.id]),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("task_list"))

    fetched_task = task_service.get_object(task.id)
    assert fetched_task is not None
    assert fetched_task.id == task.id


@login_and_return_user
@pytest.mark.django_db
def test_task_delete_with_login_with_permission(
        client,
        task_service: TaskService,  # noqa: F811
        **kwargs
):
    current_user = kwargs['login_user']

    task = TaskModelFactory.create(author=current_user)

    response = client.post(
        reverse("task_delete", args=[task.id]),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse("task_list"))

    with pytest.raises(Http404):
        task_service.get_object(task.id)
