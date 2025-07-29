from notifications.models import Notification
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SurveyInvitationSerializer(serializers.ModelSerializer):
    survey_title = serializers.CharField(source="survey.title", read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = (
            "token",
            "sent_at",
            "opened_at",
            "responded_at",
            "reminder_count",
        )


class NotificationSerializer(serializers.ModelSerializer):
    survey_title = serializers.CharField(source="survey.title", read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = (
            "token",
            "sent_at",
            "opened_at",
            "responded_at",
        )


class SurveySendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "email",
            # "user_id",
        )

    def validate(self, attrs):
        errors = {}

        # if "email" not in attrs and "user_id" not in attrs:
        #     errors.setdefault("email", []).append(REQUIRED_FIELD)

        if errors:
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data):
        validated_data["survey"] = self.context["survey_obj"]
        return super().create(validated_data)


class SurveyInvitationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "email",
        )
        read_only_fields = fields
