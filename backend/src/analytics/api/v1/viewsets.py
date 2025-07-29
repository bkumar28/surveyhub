from analytics.api.v1.serializers import (
    QuestionAnalyticsSerializer,
    SurveyAnalyticsSerializer,
)
from analytics.models import QuestionAnalytics, SurveyAnalytics
from rest_framework import permissions, viewsets


class SurveyAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SurveyAnalytics.objects.all()
    serializer_class = SurveyAnalyticsSerializer
    permission_classes = [permissions.AllowAny]


class QuestionAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuestionAnalytics.objects.all()
    serializer_class = QuestionAnalyticsSerializer
    permission_classes = [permissions.AllowAny]
