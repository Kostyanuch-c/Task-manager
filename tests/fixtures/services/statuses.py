import pytest

from task_manager.tasks.entities.status_entity import StatusInput
from task_manager.tasks.services.status_service import StatusService


@pytest.fixture
def status_service() -> StatusService:
    return StatusService()


@pytest.fixture()
def status_create_data() -> StatusInput:
    return StatusInput(
        name="new_name",
    )
