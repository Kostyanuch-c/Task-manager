from django.utils.translation.trans_real import gettext as _


class StatusTitleIsNotFreeException(Exception):
    @property
    def message(self):
        return _("Status with this name already exists")


class StatusDeleteProtectedError(Exception):
    @property
    def message(self):
        return _("Cannot delete status because it is in use")
