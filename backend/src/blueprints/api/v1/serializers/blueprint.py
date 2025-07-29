from blueprints.models import QuestionBlueprint, SurveyBlueprint
from rest_framework import serializers


class SurveyBlueprintSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = SurveyBlueprint
        fields = "__all__"
        read_only_fields = ("usage_count", "created_at")


class QuestionBlueprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBlueprint
        fields = "__all__"
        read_only_fields = ("usage_count",)
