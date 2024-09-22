import pytest

from task_manager.tasks.entities.label_entity import LabelInput
from task_manager.tasks.services.label_service import LabelService


@pytest.fixture
def label_service() -> LabelService:
    return LabelService()


@pytest.fixture()
def label_create_data() -> LabelInput:
    return LabelInput(
        name="new_name",
    )
