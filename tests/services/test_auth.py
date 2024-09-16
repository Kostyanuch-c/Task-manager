from unittest.mock import patch

from django.http import HttpRequest

from tests.fixtures.auth_service import (  # noqa
    auth_service,
    mock_request,
)

from task_manager.users.services.auth_service import AuthService


@patch("task_manager.users.services.auth_service.login")
@patch("task_manager.users.services.auth_service.authenticate")
def test_login_user_correct(
    mock_authenticate,
    mock_login,
    auth_service: AuthService,
    mock_request: HttpRequest,
):
    auth_service.login_user(
        request=mock_request,
        username="test_username",
        password="test_password",
    )

    mock_authenticate.assert_called_once_with(
        request=mock_request,
        username="test_username",
        password="test_password",
    )
    mock_login.assert_called_once_with(
        request=mock_request,
        user=mock_authenticate.return_value,
    )


@patch("task_manager.users.services.auth_service.login")
@patch("task_manager.users.services.auth_service.authenticate")
def test_login_user_wrong(
    mock_authenticate,
    mock_login,
    auth_service: AuthService,
    mock_request: HttpRequest,
):
    mock_authenticate.return_value = None

    auth_service.login_user(
        request=mock_request,
        username="wrong_username",
        password="wrong_password",
    )

    mock_authenticate.assert_called_once_with(
        request=mock_request,
        username="wrong_username",
        password="wrong_password",
    )

    mock_login.assert_not_called()


@patch("task_manager.users.services.auth_service.logout")
def test_logout_user(
    mock_logout,
    auth_service: AuthService,
    mock_request: HttpRequest,
):
    auth_service.logout_user(mock_request)
    mock_logout.assert_called_once_with(mock_request)
