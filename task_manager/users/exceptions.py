from django.utils.translation.trans_real import gettext as _


class ServiceNotDefinedError(Exception):
    @property
    def message(self):
        return _("Service not defined")


class UsernameIsNotFreeException(Exception):
    @property
    def message(self):
        return _("Username is already taken.")


class UserDeleteProtectedError(Exception):
    @property
    def message(self):
        return _("Cannot delete user because it is in use")
