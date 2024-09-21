from django.http import Http404

import pytest
from tests.factories.tasks import TaskModelFactory
from tests.fixtures.services.tasks import (  # noqa
    task_create_data,
    task_service,
)

from task_manager.tasks.entities.task_entity import TaskInput
from task_manager.tasks.exceptions.task_exceptions import (
    TaskNameIsNotFreeException,
)
from task_manager.tasks.services.task_service import TaskService


@pytest.mark.django_db
def test_get_task_all_without_filters(task_service: TaskService):
    expected_count = 3
    tasks = TaskModelFactory.create_batch(expected_count)
    names = {task.name for task in tasks}
    fetched_tasks = task_service.get_all_objects()
    fetched_names = {task.name for task in fetched_tasks}
    assert len(fetched_tasks) == expected_count
    assert names == fetched_names


@pytest.mark.django_db
def test_create_task(
        task_service: TaskService,
        task_create_data: TaskInput,
):
    task_service.create_object(task_create_data)
    fetched_task = task_service.get_all_objects()[0]
    assert fetched_task is not None
    assert fetched_task.name == task_create_data.name
    assert fetched_task.description == task_create_data.description
    assert fetched_task.status == task_create_data.status
    assert fetched_task.author == task_create_data.author
    assert fetched_task.executor == task_create_data.executor


@pytest.mark.django_db
def test_create_status_name_already_exists(
        task_service: TaskService,
        task_create_data: TaskInput,
):
    TaskModelFactory.create(name=task_create_data.name)

    with pytest.raises(TaskNameIsNotFreeException):
        task_service.create_object(task_create_data)


@pytest.mark.django_db
def test_update_task(
        task_service: TaskService,
        task_create_data: TaskInput,
):
    task = TaskModelFactory.create()

    task_service.update_object(task.id, task_create_data)

    fetched_task = task_service.get_object(task.id)
    assert fetched_task.name == task_create_data.name
    assert fetched_task.description == task_create_data.description
    assert fetched_task.status == task_create_data.status
    assert fetched_task.author == task_create_data.author
    assert fetched_task.executor == task_create_data.executor


@pytest.mark.django_db
def test_update_status_name_already_exists(
        task_service: TaskService,
        task_create_data: TaskInput,
):
    task = TaskModelFactory.create(name=task_create_data.name)

    with pytest.raises(TaskNameIsNotFreeException):
        task_service.update_object(task.id, task_create_data)


@pytest.mark.django_db
def test_delete_task(task_service: TaskService):
    task = TaskModelFactory.create()

    task_service.delete_object(task.id)
    tasks = task_service.get_all_objects()

    assert len(tasks) == 0
    with pytest.raises(Http404):
        task_service.get_object(task.id)
