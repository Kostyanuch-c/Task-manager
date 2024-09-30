import factory

from task_manager.labels.models import Label


class LabelModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Label

    name = factory.Faker("word")
