import logging

from core.api_message import EXTRA_FIELD_CONTAIN, REQUIRED_FIELD
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from surveys.models.question import Question
from surveys.models.survey import Survey

logger = logging.getLogger(__name__)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ["survey"]  # Make survey read-only

    def create(self, validated_data):
        # Get survey from URL if not explicitly provided
        if (
            "survey" not in validated_data
            and "view" in self.context
            and "survey_pk" in self.context.get("view").kwargs
        ):
            survey_pk = self.context.get("view").kwargs.get("survey_pk")
            try:
                logger.info(f"Getting survey from URL parameter: {survey_pk}")
                survey = Survey.objects.get(pk=survey_pk)
                validated_data["survey"] = survey
            except Survey.DoesNotExist:
                logger.error(f"Survey with ID {survey_pk} does not exist")
                raise serializers.ValidationError(
                    {"survey": f"Survey with ID {survey_pk} does not exist"}
                )

        return super().create(validated_data)


class QuestionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "title", "field_type", "is_required")
        read_only_fields = fields


class QuestionBulkActionSerializer(serializers.ListSerializer):
    def create_question(self, validated_data, survey_obj):
        """
         Create survey question
        :param validated_data:
        :param survey_obj:
        :return:
        """
        for question_data_obj in validated_data:
            # set survey object
            question_data_obj["survey_id"] = survey_obj

            # create question
            Question.objects.create(**question_data_obj)

    def batch_question_func(self, validated_data, survey_obj):
        """
        This function will validate the question action type and perform the
        operations according. it will perform add, update and delete actions.
        :param validated_data:
        :param survey_obj:
        :return:
        """
        for question_data_obj in validated_data:
            if (
                "action_type" in question_data_obj
                and question_data_obj["action_type"] == "DELETE"
            ):
                # delete survey question
                question_data_obj["id"].delete()
                continue

            elif (
                "action_type" in question_data_obj
                and question_data_obj["action_type"] == "POST"
            ):
                del question_data_obj["action_type"]

                # add new survey question
                self.create_question([question_data_obj], survey_obj)
                continue

            if "action_type" in question_data_obj:
                del question_data_obj["action_type"]

            instance = question_data_obj.pop("id")

            for key, value in question_data_obj.items():
                setattr(instance, key, value)

            instance.save()


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "title",
            "field_type",
            "is_required",
        )
        list_serializer_class = QuestionBulkActionSerializer


class QuestionCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    ACTION_TYPE_CHOICE = (
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
    )

    id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    action_type = serializers.ChoiceField(choices=ACTION_TYPE_CHOICE, required=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "title",
            "field_type",
            "is_required",
            "action_type",
        )
        list_serializer_class = QuestionBulkActionSerializer

    def validate(self, attrs):
        errors = {}

        if "action_type" not in attrs:
            errors.setdefault("action_type", []).append(REQUIRED_FIELD)

        if "action_type" in attrs:
            if attrs["action_type"] == "POST":
                if "title" not in attrs:
                    errors.setdefault("title", []).append(REQUIRED_FIELD)

                if "field_type" not in attrs:
                    errors.setdefault("field_type", []).append(REQUIRED_FIELD)

                if "id" in attrs:
                    errors.setdefault("id", []).append(EXTRA_FIELD_CONTAIN)

            elif attrs["action_type"] in ["PUT", "DELETE"]:
                if "id" not in attrs:
                    errors.setdefault("id", []).append(REQUIRED_FIELD)
        if errors:
            raise ValidationError(errors)

        return attrs
