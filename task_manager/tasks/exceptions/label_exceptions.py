from django.utils.translation.trans_real import gettext as _


class LabelNameIsNotFreeException(Exception):
    message = _("Label with this name already exists")


class LabelDeleteProtectedError(Exception):
    message = _("Cannot delete label because it is in use")
