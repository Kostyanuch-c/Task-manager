from abc import (
    ABC,
    abstractmethod,
)

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.http import HttpRequest


class BaseAuthService(ABC):
    @abstractmethod
    def login_user(
        self,
        request: HttpRequest,
        username: str,
        password: str,
    ) -> bool:
        ...

    @abstractmethod
    def logout_user(self, request: HttpRequest) -> None:
        ...


class AuthService(BaseAuthService):
    def login_user(
        self,
        request: HttpRequest,
        username: str,
        password: str,
    ) -> bool:

        user = authenticate(
            request=request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request=request, user=user)
            return True
        return False

    def logout_user(self, request: HttpRequest) -> None:
        logout(request)
