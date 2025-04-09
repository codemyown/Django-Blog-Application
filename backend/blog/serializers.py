from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Author, Comment, Post


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates password and creates user.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Converts Author instances to/from JSON, includes user, bio, profile picture, and website.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Author
        fields = [
            "id",
            "user",
            "bio",
            "profile_picture",
            "website",
            "created_at",
            "updated_at",
        ]


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    Handles converting post data to/from JSON format.
    """

    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "image",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at"]
        read_only_fields = ["id", "post", "author", "created_at"]
