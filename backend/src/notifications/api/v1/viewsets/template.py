from notifications.api.v1.serializers.template import NotificationTemplateSerializer
from notifications.models import NotificationTemplate
from rest_framework import viewsets


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = []  # Allow any for testing
