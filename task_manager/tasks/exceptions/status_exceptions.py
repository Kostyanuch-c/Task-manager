from django.utils.translation.trans_real import gettext as _


class StatusTitleIsNotFreeException(Exception):
    message = _("Status with this name already exists")


class StatusDeleteProtectedError(Exception):
    message = _("Cannot delete status because it is in use")
