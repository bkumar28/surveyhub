from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Frontend auth pages
    path("login/", TemplateView.as_view(template_name="auth/login.html"), name="login"),
    # JWT endpoints
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/token/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
