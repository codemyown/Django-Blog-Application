import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_user_register():
    client = APIClient()
    data = {"username": "newuser", "email": "new@test.com", "password": "newpass123"}
    response = client.post("/api/register/", data)
    assert response.status_code == 201
    assert User.objects.filter(username="newuser").exists()
