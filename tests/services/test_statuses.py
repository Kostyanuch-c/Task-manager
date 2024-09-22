from django.http import Http404

import pytest
from tests.factories.statuses import StatusModelFactory
from tests.factories.tasks import TaskModelFactory
from tests.fixtures.services.statuses import (  # noqa
    status_create_data,
    status_service,
)

from task_manager.tasks.entities.status_entity import StatusInput
from task_manager.tasks.exceptions.status_exceptions import (
    StatusDeleteProtectedError,
    StatusTitleIsNotFreeException,
)
from task_manager.tasks.services.status_service import StatusService


@pytest.mark.django_db
def test_get_status_all(status_service: StatusService):
    expected_count = 3
    status = StatusModelFactory.create_batch(expected_count)
    names = {status.name for status in status}

    fetched_statuses = status_service.get_all_objects()
    fetched_names = {status.name for status in fetched_statuses}
    assert len(fetched_statuses) == expected_count
    assert names == fetched_names


@pytest.mark.django_db
def test_create_status(
        status_service: StatusService,
        status_create_data: StatusInput,
):
    status_service.create_object(status_create_data)
    fetched_status = status_service.get_all_objects()[0]
    assert fetched_status is not None
    assert (
        fetched_status.name == status_create_data.name,
    )


@pytest.mark.django_db
def test_create_status_name_already_exists(
        status_service: StatusService,
        status_create_data: StatusInput,
):
    StatusModelFactory.create(name="new_name")

    with pytest.raises(StatusTitleIsNotFreeException):
        status_service.create_object(status_create_data)


@pytest.mark.django_db
def test_update_status_correct(
        status_service: StatusService,
        status_create_data: StatusInput,
):
    status = StatusModelFactory.create()

    status_service.update_object(status.id, status_create_data)

    fetched_status = status_service.get_object(status.id)

    assert fetched_status.name == status_create_data.name
    assert fetched_status.created_at == status.created_at
    assert fetched_status.id == status.id


@pytest.mark.django_db
def test_update_status_name_already_exists(
        status_service: StatusService,
        status_create_data: StatusInput,
):
    status = StatusModelFactory.create(
        name="new_name",
    )
    with pytest.raises(StatusTitleIsNotFreeException):
        status_service.update_object(status.id, status_create_data)


@pytest.mark.django_db
def test_delete_status(status_service: StatusService):
    status = StatusModelFactory.create()

    status_service.delete_object(status.id)
    statuses = status_service.get_all_objects()

    assert len(statuses) == 0

    with pytest.raises(Http404):
        status_service.get_object(status.id)


@pytest.mark.django_db
def test_delete_status_when_using(status_service: StatusService):
    status = StatusModelFactory.create()
    TaskModelFactory.create(status=status)

    with pytest.raises(StatusDeleteProtectedError):
        status_service.delete_object(status.id)
