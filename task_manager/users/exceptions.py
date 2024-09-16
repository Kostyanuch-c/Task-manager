from django.utils.translation.trans_real import gettext as _


class UsernameIsNotFreeException(Exception):
    @property
    def message(self):
        return _("Username is already taken.")


class ServiceNotDefinedError(Exception):
    @property
    def message(self):
        return _("Service not defined")
