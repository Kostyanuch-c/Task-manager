from unittest.mock import MagicMock

from django.http import HttpRequest

import pytest

from task_manager.users.services.auth_service import (
    AuthService,
    BaseAuthService,
)


@pytest.fixture
def auth_service() -> BaseAuthService:
    return AuthService()


@pytest.fixture
def mock_request() -> MagicMock:
    return MagicMock(scep=HttpRequest)
