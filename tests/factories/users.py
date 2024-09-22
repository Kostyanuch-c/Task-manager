from django.contrib.auth import get_user_model

import factory


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    password = factory.django.Password("pw")
