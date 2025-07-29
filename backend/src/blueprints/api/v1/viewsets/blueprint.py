from blueprints.api.v1.serializers.blueprint import (
    QuestionBlueprintSerializer,
    SurveyBlueprintSerializer,
)
from blueprints.models import QuestionBlueprint, SurveyBlueprint
from core.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, viewsets


class SurveyBlueprintViewSet(viewsets.ModelViewSet):
    queryset = SurveyBlueprint.objects.all()
    serializer_class = SurveyBlueprintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuestionBlueprintViewSet(viewsets.ModelViewSet):
    queryset = QuestionBlueprint.objects.all()
    serializer_class = QuestionBlueprintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
