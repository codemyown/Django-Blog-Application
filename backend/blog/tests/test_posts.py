import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from blog.models import Author, Post


@pytest.mark.django_db
def create_user_and_login():
    user = User.objects.create_user(username="testuser", password="testpass123")
    Author.objects.create(user=user)
    client = APIClient()
    response = client.post(
        "/api/token/", {"username": "testuser", "password": "testpass123"}
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


@pytest.mark.django_db
def test_create_post():
    client, user = create_user_and_login()
    data = {
        "title": "My First Post",
        "content": "This is the content.",
    }
    response = client.post("/posts/", data)
    assert response.status_code == 201
    assert Post.objects.filter(title="My First Post").exists()


@pytest.mark.django_db
def test_list_posts():
    client, user = create_user_and_login()
    Post.objects.create(author=user.author, title="Sample", content="Sample content")
    response = client.get("/posts/")
    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_retrieve_post_detail():
    client, user = create_user_and_login()
    post = Post.objects.create(
        author=user.author, title="Detail Post", content="Some content"
    )
    response = client.get(f"/posts/{post.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Detail Post"


@pytest.mark.django_db
def test_update_post():
    client, user = create_user_and_login()
    post = Post.objects.create(
        author=user.author, title="Old Title", content="Old content"
    )
    data = {"title": "New Title", "content": "Updated content"}
    response = client.put(f"/posts/{post.id}/", data)
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.title == "New Title"


@pytest.mark.django_db
def test_delete_post():
    client, user = create_user_and_login()
    post = Post.objects.create(
        author=user.author, title="To Be Deleted", content="Gone soon"
    )
    response = client.delete(f"/posts/{post.id}/")
    assert response.status_code == 204
    assert not Post.objects.filter(id=post.id).exists()
