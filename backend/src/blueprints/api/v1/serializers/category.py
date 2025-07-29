from blueprints.models import BlueprintCategory
from rest_framework import serializers


class BlueprintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueprintCategory
        fields = "__all__"
