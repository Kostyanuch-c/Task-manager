from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    surname = models.CharField(max_length=50, verbose_name=_('Surname'))
    username = models.CharField(
        max_length=150, unique=True, null=False, blank=False, verbose_name=_('Username'),
        help_text=_(
            'Required field. 150 characters or fewer. '
            'Password must contain only letters, numbers and symbols @/./+/-/_.'),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Zа-яА-Я0-9+_@.-]*$',
                message=_('Invalid characters included'),
            ),
            MaxLengthValidator(150, message=_('Max length is 150 characters')),
        ])
    password = models.CharField(
        null=False, blank=False, verbose_name=_('Password'),
        help_text=_('Your password must contain at least 3 characters'),
        validators=[
            MinLengthValidator(3, message=_('Must be at least 3 characters')),
        ])

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
