import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """A simple API client for testing."""
    return APIClient()
