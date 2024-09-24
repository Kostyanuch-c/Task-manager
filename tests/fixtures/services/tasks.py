import pytest
from tests.factories.labels import LabelModelFactory
from tests.factories.statuses import StatusModelFactory
from tests.factories.users import UserModelFactory

from task_manager.tasks.entities.task_entity import TaskInput
from task_manager.tasks.services.task_service import TaskService


@pytest.fixture
def task_service() -> TaskService:
    return TaskService()


@pytest.fixture()
def task_create_data() -> TaskInput:
    return TaskInput(
        name="task_nAme_",
        description="description",
        status=StatusModelFactory.create(),
        author=UserModelFactory.create(),
        executor=UserModelFactory.create(),
        label=[LabelModelFactory.create(), LabelModelFactory.create()],
    )
