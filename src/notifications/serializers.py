from rest_framework import serializers

from .models import NotificationTemplate, SurveyInvitation


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"
        read_only_fields = ("created_at",)


class SurveyInvitationSerializer(serializers.ModelSerializer):
    survey_title = serializers.CharField(source="survey.title", read_only=True)

    class Meta:
        model = SurveyInvitation
        fields = "__all__"
        read_only_fields = (
            "token",
            "sent_at",
            "opened_at",
            "responded_at",
            "reminder_count",
        )
