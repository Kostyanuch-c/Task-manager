from django.utils.translation.trans_real import gettext as _


class LabelNameIsNotFreeException(Exception):
    @property
    def message(self):
        return _("Label with this name already exists")


class LabelDeleteProtectedError(Exception):
    @property
    def message(self):
        return _("Cannot delete label because it is in use")
