from rest_framework import viewsets, permissions
from .models import NotificationTemplate, SurveyInvitation
from .serializers import NotificationTemplateSerializer, SurveyInvitationSerializer
from src.core.permissions import IsStaffOrReadOnly


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsStaffOrReadOnly]


class SurveyInvitationViewSet(viewsets.ModelViewSet):
    queryset = SurveyInvitation.objects.select_related('survey').all()
    serializer_class = SurveyInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
