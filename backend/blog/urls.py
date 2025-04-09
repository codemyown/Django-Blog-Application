from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from blog.views import (
    AuthorAPIView,
    CommentListCreateAPIView,
    HealthCheckView,
    PostViewSet,
    ReadinessCheckView,
    RegisterView,
)

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")


urlpatterns = [
    path("", include(router.urls)),
    path("author/", AuthorAPIView.as_view(), name="author"),
    path(
        "posts/<int:post_id>/comments/",
        CommentListCreateAPIView.as_view(),
        name="post_comments",
    ),
    path("api/register/", RegisterView.as_view(), name="register_user"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("health/", HealthCheckView.as_view(), name="health"),
    path("readiness/", ReadinessCheckView.as_view(), name="readiness"),
]
