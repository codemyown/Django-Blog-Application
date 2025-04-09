from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    """
    Represents a blog author linked to a Django User.

    Attributes:
        user (OneToOneField): Links to Django's User model.
        bio (TextField): Short biography of the author.
        profile_picture (ImageField): Optional profile picture.
        website (URLField): Personal website URL.
        created_at (DateTimeField): Timestamp when the author profile was created.
        updated_at (DateTimeField): Timestamp when the author profile was last updated.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    """
    Represents a blog post written by an author.

    Attributes:
        author (ForeignKey): The author of the post.
        title (CharField): Title of the post.
        content (TextField): Full text content of the post.
        image (ImageField): Optional feature image for the post.
        created_at (DateTimeField): Timestamp when the post was created.
        updated_at (DateTimeField): Timestamp when the post was last updated.

    """

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a comment made on a post by an author.

    Attributes:
        post (ForeignKey): The post this comment belongs to.
        author (ForeignKey): The author who made the comment.
        content (TextField): The actual comment text.
        created_at (DateTimeField): Timestamp when the comment was created.
        updated_at (DateTimeField): Timestamp when the comment was last updated.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
