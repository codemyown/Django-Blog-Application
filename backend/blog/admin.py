from django.contrib import admin

from .models import Author, Comment, Post


class AuthorAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Author model.

    list_display: Specifies the fields to display in the list view.
    search_fields: Allows searching authors by username, bio, and website.
    list_filter: Adds filters for created and updated timestamps.
    readonly_fields: Prevents editing of created_at and updated_at fields.
    """

    list_display = ("user", "bio", "website", "created_at", "updated_at")
    search_fields = ("user__username", "bio", "website")
    list_filter = ("created_at", "updated_at")
    readonly_fields = (
        "created_at",
        "updated_at",
    )


class PostAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Post model.

    list_display: Specifies the fields to display in the list view.
    search_fields: Allows searching posts by title, content, and author's username.
    list_filter: Adds filters for created and updated timestamps.
    readonly_fields: Prevents editing of created_at and updated_at fields.
    """

    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "content", "author__user__username")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


class CommentAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Comment model.

    list_display: Specifies the fields to display in the list view.
    search_fields: Allows searching comments by author's username, post title, and content.
    list_filter: Adds a filter for created_at timestamp.
    readonly_fields: Prevents editing of created_at field.
    """

    list_display = ("author", "post", "created_at")
    search_fields = ("author__user__username", "post__title", "content")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
