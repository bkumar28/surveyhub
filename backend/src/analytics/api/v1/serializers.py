from analytics.models import QuestionAnalytics, SurveyAnalytics
from rest_framework import serializers


class SurveyAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnalytics
        fields = "__all__"
        read_only_fields = ("id", "survey", "updated_at")


class QuestionAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnalytics
        fields = "__all__"
        read_only_fields = ("id", "question", "updated_at")
