import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_register(api_client):
    """Test registering a new user."""
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test@123",
        "role": "customer"   # optional, matches your serializer
    }
    
    response = api_client.post(reverse("register"), payload, format="json")
    
    assert response.status_code == 201
    assert response.data["email"] == payload["email"]
    assert response.data["username"] == payload["username"]
