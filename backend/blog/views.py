from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Comment, Post
from .serializers import (
    AuthorSerializer,
    CommentSerializer,
    PostSerializer,
    RegisterSerializer,
)


class RegisterView(APIView):
    """
    POST /api/register/

    Registers a new user and creates an Author profile.
    No authentication required.

    Returns:
        201 - User registered successfully
        400 - Validation errors
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        Register a new user.

        Creates user and author if data is valid.
        Returns success or error response.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Author.objects.create(user=user)
            return Response(
                {"msg": "User registered successfully."}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorAPIView(APIView):
    """
    Author API View

    Handles retrieving,  updating
    the authenticated user's author profile.

    Endpoints:
        GET    /authors/         - Retrieve your author profile
        PUT    /authors/         - Update your author profile

    Permissions:
        - Must be authenticated
        - Can only manage your own profile
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get the logged-in user's author profile.

        Returns author data or not found message.
        """
        author = Author.objects.filter(user=request.user).first()
        if not author:
            return Response({"detail": "Author profile not found."}, status=404)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request):
        """
        Update the logged-in user's author profile.

        Returns updated data or errors.
        """
        author = Author.objects.filter(user=request.user).first()
        if not author:
            return Response(
                {"detail": "Author profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    """
    Post ViewSet

    Authenticated users can create, view, update, and delete their own posts.

    Endpoints:
        GET    /posts/         - List user's posts
        POST   /posts/         - Create a post
        GET    /posts/<id>/    - Retrieve a post
        PUT    /posts/<id>/    - Update a post (owner only)
        DELETE /posts/<id>/    - Delete a post (owner only)
        GET    /posts/my/       - List only user's uploaded posts
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get all posts.
        """
        return Post.objects.all()

    def perform_create(self, serializer):
        """
        Save a new post with the logged-in user as author.
        """
        image = self.request.FILES.get("image")
        author = getattr(self.request.user, "author", None)
        if not author:
            Author.objects.create(user=self.request.user)
        serializer.save(author=self.request.user.author, image=image)

    def check_author_permission(self, post):
        """
        Check if the logged-in user is the post's author.
        """
        if post.author != self.request.user.author:
            raise PermissionDenied("You can only modify your own posts.")

    def update(self, request, *args, **kwargs):
        """
        Update a post if the user is the author.
        """

        post = self.get_object()
        self.check_author_permission(post)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a post if the user is the author.
        """
        post = self.get_object()
        self.check_author_permission(post)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="my")
    def my_posts(self, request):
        """
        List posts created by the logged-in user.
        """
        posts = Post.objects.filter(author=request.user.author)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class CommentListCreateAPIView(ListCreateAPIView):
    """
    Comment ListCreateAPIView

    Allows viewing and adding comments to a specific blog post.

    Endpoints:
        GET  /posts/<id>/comments/   - List all comments for the given post
        POST /posts/<id>/comments/   - Add a comment to the post (auth required)
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns all comments related to the specified post.
        Raises 404 if the post does not exist.
        """
        post_id = self.kwargs["post_id"]
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post not found.")
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        """
        Creates a new comment for the specified post using the authenticated user as the author.
        """
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(pk=post_id)
        author = self.request.user.author
        serializer.save(post=post, author=author)


class HealthCheckView(APIView):
    """
    Returns API health status.
    Used for uptime monitoring.

    - GET /health/ → { "status": "ok" }
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Health check endpoint. Returns status OK.
        """
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ReadinessCheckView(APIView):
    """
    Returns API readiness status.
    Used by Kubernetes for readiness probes.

    - GET /readiness/ → { "status": "ready" }
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Readiness check endpoint. Returns status ready.
        """
        return Response({"status": "ready"}, status=status.HTTP_200_OK)
