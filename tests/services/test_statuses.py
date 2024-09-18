from django.http import Http404

import pytest
from tests.factories.statuses import StatusModelFactory
from tests.fixtures.services.statuses import (  # noqa
    status_create_data,
    status_service,
)

from task_manager.tasks.entities.status_entity import StatusInputEntity
from task_manager.tasks.exceptions.status_exceptions import (
    StatusTitleIsNotFreeException,
)
from task_manager.tasks.services.status_service import StatusService


@pytest.mark.django_db
def test_get_status_all(status_service: StatusService):
    expected_count = 5
    status = StatusModelFactory.create_batch(expected_count)
    titles = {status.title for status in status}

    fetched_statuses = status_service.get_all_objects()
    fetched_titles = {status.title for status in fetched_statuses}
    assert len(fetched_statuses) == expected_count
    assert titles == fetched_titles


@pytest.mark.django_db
def test_create_status(
        status_service: StatusService,
        status_create_data: StatusInputEntity,
):
    fetched_status = status_service.create_object(status_create_data)
    assert fetched_status is not None
    assert fetched_status.title == status_create_data.title, f"{fetched_status.title=}"


@pytest.mark.django_db
def test_create_status_title_already_exists(
        status_service: StatusService,
        status_create_data: StatusInputEntity,
):
    StatusModelFactory.create(title='new_title')

    with pytest.raises(StatusTitleIsNotFreeException):
        status_service.create_object(status_create_data)


@pytest.mark.django_db
def test_update_user_correct(
        status_service: StatusService,
        status_create_data: StatusInputEntity,
):
    status = StatusModelFactory.create()

    status_service.update_object(status.id, status_create_data)

    fetched_status = status_service.get_object(status.id)

    assert fetched_status.title == status_create_data.title
    assert fetched_status.created_at == status.created_at
    assert fetched_status.id == status.id


@pytest.mark.django_db
def test_update_user_username_already_exists(
        status_service: StatusService,
        status_create_data: StatusInputEntity,
):
    status = StatusModelFactory.create(
        title='new_title',
    )
    with pytest.raises(StatusTitleIsNotFreeException):
        status_service.update_object(status.id, status_create_data)


@pytest.mark.django_db
def test_delete_user(status_service: StatusService):
    user = StatusModelFactory.create()

    status_service.delete_object(user.id)

    with pytest.raises(Http404):
        status_service.get_object(user.id)
