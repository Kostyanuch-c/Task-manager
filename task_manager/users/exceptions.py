from django.utils.translation.trans_real import gettext as _


class ServiceNotDefinedError(Exception):
    message = _('Service not defined')


class UsernameIsNotFreeException(Exception):
    message = _('Username is already taken')


class UserDeleteProtectedError(Exception):
    message = _("Cannot delete user because it is in use")
