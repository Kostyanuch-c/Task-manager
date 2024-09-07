from django.core.validators import MinLengthValidator
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    password = models.CharField(max_length=150, null=False, blank=False, validators=[
        MinLengthValidator(3, message="Минимальная длина ппароля 3 символа")])
