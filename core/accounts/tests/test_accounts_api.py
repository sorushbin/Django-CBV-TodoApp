from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestRegistrationApi:
    def test_registration_success(self, api_client):
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "test@example.com",
            "password": "TestPassword123",
            "password1": "TestPassword123",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_registration_passwords_do_not_match(self):
        client = APIClient()
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "test@example.com",
            "password": "TestPassword123",
            "password1": "DifferentPassword",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_weak_password(self):
        client = APIClient()
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "test@example.com",
            "password": "weak",
            "password1": "weak",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
