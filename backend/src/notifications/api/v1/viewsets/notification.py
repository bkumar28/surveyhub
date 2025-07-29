from notifications.api.v1.serializers.notification import (
    NotificationSerializer,
    SurveyInvitationSerializer,
)
from notifications.models import Notification
from rest_framework import generics, permissions, viewsets


class SurveyInvitationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related("survey").all()
    serializer_class = SurveyInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all().order_by("id")
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]
