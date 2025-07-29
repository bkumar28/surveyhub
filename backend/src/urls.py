"""surveyhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from authentication.views import RootView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Root: dashboard if logged in, else login
    path("", RootView.as_view(), name="root"),
    # Dashboard app
    path("", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("", include(("surveys.urls", "surveys"), namespace="surveys")),
    path("", include(("blueprints.urls", "blueprints"), namespace="blueprints")),
    path(
        "", include(("notifications.urls", "notifications"), namespace="notifications")
    ),
    path("", include(("analytics.urls", "analytics"), namespace="analytics")),
    # Auth API (JWT and custom)
    path(
        "",
        include(("authentication.urls", "authentication"), namespace="authentication"),
    ),
    # Accounts app
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),
]

if settings.ENABLE_MEDIA_AND_STATIC:
    # Serve static and media files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ADMIN_ENABLED:
    # Admin interface
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]

if settings.SAMPLE_DATA_STATIC_ROOT_ENABLED:
    # Serve sample data files
    urlpatterns += static(
        settings.SAMPLE_DATA_STATIC_URL, document_root=settings.SAMPLE_DATA_STATIC_PATH
    )
