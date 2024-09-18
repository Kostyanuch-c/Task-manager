from django.utils.translation.trans_real import gettext as _


class TaskNameIsNotFreeException(Exception):
    @property
    def message(self):
        return _("Task with this name already exists")
