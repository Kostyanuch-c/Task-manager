from django.http import Http404

import pytest
from tests.factories.labels import LabelModelFactory
from tests.factories.tasks import TaskModelFactory
from tests.fixtures.services.labels import (  # noqa: F401
    label_create_data,
    label_service,
)

from task_manager.tasks.entities.label_entity import LabelInput
from task_manager.tasks.exceptions.label_exceptions import (
    LabelDeleteProtectedError,
    LabelNameIsNotFreeException,
)
from task_manager.tasks.services.label_service import LabelService


@pytest.mark.django_db
def test_get_label_all(request):
    label_service_ = request.getfixturevalue("label_service")
    expected_count = 3
    label = LabelModelFactory.create_batch(expected_count)
    names = {label.name for label in label}

    fetched_label = label_service_.get_all_objects()
    fetched_names = {label.name for label in fetched_label}
    assert len(fetched_label) == expected_count
    assert names == fetched_names


@pytest.mark.django_db
def test_create_label(  # noqa: F811
        label_service: LabelService,  # noqa: F811
        label_create_data: LabelInput,  # noqa: F811
):
    label_service.create_object(label_create_data)
    fetched_label = label_service.get_all_objects()[0]
    assert fetched_label is not None
    assert fetched_label.name == label_create_data.name


@pytest.mark.django_db
def test_create_label_name_already_exists(  # noqa: F811
        label_service: LabelService,  # noqa: F811
        label_create_data: LabelInput,  # noqa: F811
):
    LabelModelFactory.create(name="new_name")

    with pytest.raises(LabelNameIsNotFreeException):
        label_service.create_object(label_create_data)


@pytest.mark.django_db
def test_delete_label(label_service: LabelService):  # noqa: F811
    label = LabelModelFactory.create()

    label_service.delete_object(label.id)
    labels = label_service.get_all_objects()

    assert len(labels) == 0

    with pytest.raises(Http404):
        label_service.get_object(label.id)


@pytest.mark.django_db
def test_delete_status(label_service: LabelService):  # noqa: F811
    label = [LabelModelFactory.create()]

    TaskModelFactory.create(labels=label)

    with pytest.raises(LabelDeleteProtectedError):
        label_service.delete_object(label[0].id)
