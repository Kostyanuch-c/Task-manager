from django.utils import timezone

import factory

from task_manager.tasks.models import Status


class StatusModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    title = factory.Faker('word')
    created_at = factory.LazyFunction(timezone.now)
