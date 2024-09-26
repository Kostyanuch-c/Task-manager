import factory

from task_manager.tasks.models import Status


class StatusModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    name = factory.Faker('word')
