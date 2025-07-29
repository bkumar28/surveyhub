from django.urls import path
from notifications.api.v1.viewsets.notification import (
    NotificationDetailView,
    NotificationListView,
)
from notifications.api.v1.viewsets.template import NotificationTemplateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"api/v1/notification-templates",
    NotificationTemplateViewSet,
    basename="notificationtemplate",
)

urlpatterns = [
    path(
        "api/v1/notifications/",
        NotificationListView.as_view(),
        name="notification-list",
    ),
    path(
        "api/v1/notifications/<uuid:pk>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),
] + router.urls
