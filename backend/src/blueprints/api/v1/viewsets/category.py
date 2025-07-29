from blueprints.api.v1.serializers.category import (
    BlueprintCategorySerializer,
)
from blueprints.models import BlueprintCategory
from rest_framework import permissions, viewsets


class BlueprintCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlueprintCategory.objects.all()
    serializer_class = BlueprintCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
