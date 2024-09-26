from unittest.mock import patch

from tests.fixtures.services.auth import (  # noqa: 401
    auth_service,
    mock_request,
)


@patch("task_manager.users.services.auth_service.login")
@patch("task_manager.users.services.auth_service.authenticate")
def test_login_user_correct(mock_authenticate, mock_login, request):
    auth_service_ = request.getfixturevalue("auth_service")
    mock_request_ = request.getfixturevalue("mock_request")

    auth_service_.login_user(
        request=mock_request_,
        username="test_username",
        password="test_password",
    )

    mock_authenticate.assert_called_once_with(
        request=mock_request_,
        username="test_username",
        password="test_password",
    )
    mock_login.assert_called_once_with(
        request=mock_request_,
        user=mock_authenticate.return_value,
    )


@patch("task_manager.users.services.auth_service.login")
@patch("task_manager.users.services.auth_service.authenticate")
def test_login_user_wrong(mock_authenticate, mock_login, request):
    auth_service_ = request.getfixturevalue("auth_service")
    mock_request_ = request.getfixturevalue("mock_request")

    mock_authenticate.return_value = None

    auth_service_.login_user(
        request=mock_request_,
        username="wrong_username",
        password="wrong_password",
    )

    mock_authenticate.assert_called_once_with(
        request=mock_request_,
        username="wrong_username",
        password="wrong_password",
    )

    mock_login.assert_not_called()


@patch("task_manager.users.services.auth_service.logout")
def test_logout_user(mock_logout, request):
    auth_service_ = request.getfixturevalue("auth_service")
    mock_request_ = request.getfixturevalue("mock_request")

    auth_service_.logout_user(mock_request_)
    mock_logout.assert_called_once_with(mock_request_)
