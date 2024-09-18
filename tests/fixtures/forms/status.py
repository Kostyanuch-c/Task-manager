import pytest


@pytest.fixture
def status_form_data() -> dict:
    return {
        'title': 'title',
    }
