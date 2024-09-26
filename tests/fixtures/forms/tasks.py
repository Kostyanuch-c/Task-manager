import pytest
from tests.factories.labels import LabelModelFactory
from tests.factories.statuses import StatusModelFactory
from tests.factories.users import UserModelFactory


@pytest.fixture
def task_form_data() -> dict:
    return {
        'name': 'form_name',
        'description': 'form_description',
        'status': StatusModelFactory.create().id,
        'executor': UserModelFactory.create().id,
        'labels': [
            LabelModelFactory.create().id,
            LabelModelFactory.create().id
        ],
    }
