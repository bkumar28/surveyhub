from rest_framework import viewsets, permissions
from .models import TemplateCategory, SurveyTemplate, QuestionTemplate
from .serializers import (
    TemplateCategorySerializer,
    SurveyTemplateSerializer,
    QuestionTemplateSerializer
)
from src.core.permissions import IsOwnerOrReadOnly

class TemplateCategoryViewSet(viewsets.ModelViewSet):
    queryset = TemplateCategory.objects.all()
    serializer_class = TemplateCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SurveyTemplateViewSet(viewsets.ModelViewSet):
    queryset = SurveyTemplate.objects.all()
    serializer_class = SurveyTemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuestionTemplateViewSet(viewsets.ModelViewSet):
    queryset = QuestionTemplate.objects.all()
    serializer_class = QuestionTemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
