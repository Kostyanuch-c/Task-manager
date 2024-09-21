from django.utils import timezone

import factory
from tests.factories.statuses import StatusModelFactory
from tests.factories.users import UserModelFactory

from task_manager.tasks.models import Task


class TaskModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Faker('word')
    description = factory.Faker('text')
    author = factory.SubFactory(UserModelFactory)
    executor = factory.SubFactory(UserModelFactory)
    status = factory.SubFactory(StatusModelFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
