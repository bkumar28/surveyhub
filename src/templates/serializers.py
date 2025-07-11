from rest_framework import serializers

from .models import QuestionTemplate, SurveyTemplate, TemplateCategory


class TemplateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateCategory
        fields = "__all__"


class SurveyTemplateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = SurveyTemplate
        fields = "__all__"
        read_only_fields = ("usage_count", "created_at")


class QuestionTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTemplate
        fields = "__all__"
        read_only_fields = ("usage_count",)
