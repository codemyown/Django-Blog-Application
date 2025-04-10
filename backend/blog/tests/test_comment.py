import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from blog.models import Author, Post


@pytest.mark.django_db
def create_user_post():
    user = User.objects.create_user(username="testuser", password="testpass123")
    author = Author.objects.create(user=user)
    post = Post.objects.create(author=author, title="Test Post", content="Post content")
    client = APIClient()
    response = client.post(
        "/api/token/", {"username": "testuser", "password": "testpass123"}
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, post, author


@pytest.mark.django_db
def test_add_comment():
    client, post, author = create_user_post()
    data = {"content": "Nice post!"}
    response = client.post(f"/posts/{post.id}/comments/", data)
    assert response.status_code == 201
    assert post.comments.count() == 1
