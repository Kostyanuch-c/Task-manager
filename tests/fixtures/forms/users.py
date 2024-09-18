import pytest


@pytest.fixture
def users_form_data() -> dict:
    return {
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "newusername",
        "password1": 12345,
        "password2": 12345,
    }
