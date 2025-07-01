from rest_framework import permissions, viewsets

from src.core.permissions import IsStaffOrReadOnly

from .models import NotificationTemplate, SurveyInvitation
from .serializers import NotificationTemplateSerializer, SurveyInvitationSerializer


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsStaffOrReadOnly]


class SurveyInvitationViewSet(viewsets.ModelViewSet):
    queryset = SurveyInvitation.objects.select_related("survey").all()
    serializer_class = SurveyInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
