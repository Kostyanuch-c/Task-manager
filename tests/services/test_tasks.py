from django.http import Http404

import pytest
from tests.factories.labels import LabelModelFactory
from tests.factories.tasks import TaskModelFactory
from tests.fixtures.services.tasks import (
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
    labels1 = LabelModelFactory.create_batch(2)
    task1 = TaskModelFactory.create(labels=labels1, name='first task')

    labels2 = LabelModelFactory.create_batch(2)
    task2 = TaskModelFactory.create(labels=labels2, name='second task')

    names = {task.name for task in (task1, task2)}
    label_names = [{label.name for label in list(task.labels.all())} for task in (task1, task2)]

    fetched_tasks = task_service.get_all_objects()
    fetched_task_names = {task.name for task in (task1, task2)}
    fetched_labels_names = [
        {label.name for label in list(task.labels.all())}
        for task in fetched_tasks
    ]

    assert names == fetched_task_names
    assert label_names[0] == fetched_labels_names[0]
    assert label_names[1] == fetched_labels_names[1]


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
    assert {label.name for label in fetched_task.labels.all()} == {
        label.name for label in task_create_data.labels
    }


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
    label = [LabelModelFactory.create(name='create_label')]
    task = TaskModelFactory.create(labels=label, name='task_name')

    task_service.update_object(task.id, task_create_data)

    fetched_task = task_service.get_object(task .id)

    new_labels = {label.name for label in fetched_task.labels.all()}
    assert fetched_task.name == task_create_data.name
    assert fetched_task.description == task_create_data.description
    assert fetched_task.status == task_create_data.status
    assert fetched_task.author == task_create_data.author
    assert fetched_task.executor == task_create_data.executor
    assert new_labels == {label.name for label in task_create_data.labels}
    assert 'create_label' not in new_labels

@pytest.mark.django_db
def test_update_task_name_already_exists(
        task_service: TaskService,
        task_create_data: TaskInput,
):
    task = TaskModelFactory.create(name='name')
    TaskModelFactory.create(name=task_create_data.name)

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
