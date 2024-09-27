from django.utils.translation.trans_real import gettext as _


class TaskNameIsNotFreeException(Exception):
    message = _("Task with this name already exists")
