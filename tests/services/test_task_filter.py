import pytest
from tests.factories.labels import LabelModelFactory
from tests.factories.statuses import StatusModelFactory
from tests.factories.tasks import TaskModelFactory
from tests.factories.users import UserModelFactory
from tests.fixtures.services.tasks import (  # noqa: F401
    task_service,
)

from task_manager.tasks.services.task_service import TaskService


@pytest.mark.django_db
def test_get_task_only_user_tasks(task_service: TaskService):  # noqa: F811
    user = UserModelFactory.create()

    TaskModelFactory.create(name='name1')
    TaskModelFactory.create(name='name2')
    TaskModelFactory.create(name='name3')
    task_current_user = TaskModelFactory.create(author=user)

    fetched_tasks = task_service.get_all_objects()

    assert len(fetched_tasks) == 4
    query_params = {
        'self_tasks': 'on',
    }

    filters_tasks = task_service.get_all_objects(query_params, user.id)

    assert len(filters_tasks) == 1
    assert filters_tasks[0].id == task_current_user.id


@pytest.mark.django_db
def test_get_task_status_filter(task_service: TaskService):  # noqa: F811
    status = StatusModelFactory.create()

    TaskModelFactory.create(name='name1')
    TaskModelFactory.create(name='name2')
    TaskModelFactory.create(name='name3')

    fetched_task = TaskModelFactory.create(status=status)

    query_params = {
        'status': f'{status.id}',
    }

    filters_tasks = task_service.get_all_objects(query_params)

    assert len(filters_tasks) == 1
    assert filters_tasks[0].id == fetched_task.id


@pytest.mark.django_db
def test_get_task_executor_filter(task_service: TaskService):  # noqa: F811
    executor = UserModelFactory.create()

    TaskModelFactory.create(name='name1')
    TaskModelFactory.create(name='name2')
    TaskModelFactory.create(name='name3')

    fetched_task = TaskModelFactory.create(executor=executor)

    query_params = {
        'executor': f'{executor.id}',
    }

    filters_tasks = task_service.get_all_objects(query_params)

    assert len(filters_tasks) == 1
    assert filters_tasks[0].id == fetched_task.id


@pytest.mark.django_db
def test_get_task_label_filter(task_service: TaskService):  # noqa: F811
    label = [
        LabelModelFactory.create(name='label1'),
        LabelModelFactory.create(name='label2'),
        LabelModelFactory.create(name='label3'),
    ]

    TaskModelFactory.create(name="name1", labels=label)
    TaskModelFactory.create(name="name2", labels=[label[0]])
    TaskModelFactory.create(name="name3", labels=[label[-1]])

    query_params = {
        'label': f"{label[0].id}",
    }

    filters_tasks = task_service.get_all_objects(query_params)

    assert len(filters_tasks) == 2

    fetched_labels = [
        {label.name for label in task.labels.all()}
        for task in filters_tasks
    ]
    assert all(map(lambda labels: label[0].name in labels, fetched_labels))


@pytest.mark.django_db
def test_get_task_with_all_filters(task_service: TaskService):  # noqa: F811
    author = UserModelFactory.create()
    executor = UserModelFactory.create()
    status = StatusModelFactory.create(name='status')

    label = [
        LabelModelFactory.create(name='label1'),
        LabelModelFactory.create(name='label2'),
        LabelModelFactory.create(name='label3'),
    ]
    TaskModelFactory.create(labels=label, status=status, name='name1')
    TaskModelFactory.create(labels=[label[0]], author=author, name='name2')
    TaskModelFactory.create(labels=[label[-1]], executor=executor, name='name3')
    TaskModelFactory.create(
        labels=label[1:], executor=executor, author=author,
        status=status, name='name4'
    )

    query_params = {
        'label': f"{label[1].id}",
        'status': f'{status.id}',
        'executor': f'{executor.id}',
        'self_tasks': 'on',
    }

    filter_task = task_service.get_all_objects(query_params=query_params, user_id=author.id)

    assert len(filter_task) == 1

    assert filter_task[0].status.id == status.id
    assert filter_task[0].executor.id == executor.id
    assert filter_task[0].author.id == author.id

    fetched_labels = {label.name for label in filter_task[0].labels.all()}
    assert label[1].name in fetched_labels
