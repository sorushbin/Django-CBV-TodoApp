from django.urls import reverse
from rest_framework.test import APIClient
import pytest
from datetime import datetime
from accounts.models import User, Profile
from todo.models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def user():
    return User.objects.create_user(email="test@test.com", password="test@1234Ms")


@pytest.fixture
def profile(user):
    # Check if a profile already exists for the user
    existing_profile = Profile.objects.filter(user=user).first()
    if existing_profile:
        return existing_profile
    # If no profile exists, create a new one
    return Profile.objects.create(
        user=user,
        first_name="mahmoud",
        last_name="sifi",
        description="i am teacher",
        updated_date=datetime.now(),
    )


@pytest.fixture
def task(profile):
    return Task.objects.create(
        user=profile, title="test title", description="test description", done=True
    )


@pytest.mark.django_db
class TestTodoApi:

    def test_get_list_task_response_200_status(self, api_client):
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_task_unauthorized_response_401_status(self, api_client, task):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": task.title,
            "description": task.description,
            "done": task.done,
            "updated_date": task.updated_date,
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_post_task_authorized_response_201_status(self, api_client, user, task):
        url = reverse("todo:api-v1:task-list")
        data = {
            "user": task.user,
            "title": task.title,
            "description": task.description,
            "done": task.done,
            "updated_date": task.updated_date,
        }
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_delete_task_unauthorized_response_401_status(self, api_client, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.pk})
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_delete_task_authorized_response_204_status(self, api_client, user, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.pk})
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        assert response.status_code == 204
        # Verify that the task item has been deleted from the database
        with pytest.raises(Task.DoesNotExist):
            Task.objects.get(pk=task.pk)

    def test_edit_task_unauthorized_response_401_status(self, api_client, user, task):
        updated_data = {
            "title": "Updated Test Task",
            "description": "Updated test description",
            "done": True,
            "updated_date": datetime.now(),
        }

        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.pk})
        response = api_client.put(url, updated_data)
        assert response.status_code == 401

    def test_edit_task_authorized_response_200_status(self, api_client, user, task):
        api_client.force_authenticate(user=user)
        # Define the updated data for the task
        updated_data = {
            "title": "Updated Test Task",
            "description": "Updated test description",
            "done": True,
            "updated_date": datetime.now(),
        }

        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.pk})
        response = api_client.put(url, updated_data)
        assert response.status_code == 200
        # Retrieve the task from the database
        updated_task = Task.objects.get(pk=task.pk)
        # Verify that the task attributes have been updated correctly
        assert updated_task.title == updated_data["title"]
        assert updated_task.description == updated_data["description"]
        assert updated_task.done == updated_data["done"]


