import uuid

from core.api_message import (
    INVALID_SURVEY_QUESTION_ID,
    REQUIRED_FIELD,
)
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from surveys.models.answer import Answer
from surveys.models.survey import Survey


class AnswerViewSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField("get_question")
    field_type = serializers.SerializerMethodField("get_field_type")
    submitted_by = serializers.SerializerMethodField("get_submitted_by_detail")

    class Meta:
        model = Answer
        fields = (
            "id",
            "question",
            "field_type",
            # "ans",
            # "submit_date",
            # "uuid",
            "submitted_by",
        )
        read_only_fields = fields

    def get_question(self, value):
        return value.question_id.title

    @extend_schema_field(serializers.CharField)
    def get_field_type(self, value):
        return value.question_id.field_type

    # def get_submitted_by_detail(self, value):
    #     if value.invitation_id is None:
    #         return {"name": "Anonymous User"}

    #     if value.invitation_id.user_id is not None:
    #         return UserViewSerializer(value.invitation_id.user_id).data

    #     return {"email": value.invitation_id.email}


class SurveyQuestionAnswerViewSerializer(serializers.ModelSerializer):
    question_ans = serializers.SerializerMethodField("get_qt_ans")

    class Meta:
        model = Survey
        fields = (
            "id",
            "title",
            "description",
            "start_date",
            # "expired_date",
            "question_ans",
        )
        read_only_fields = fields

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_qt_ans(self, value):
        if "answers_list_obj" in self.context:
            answers_list_obj = self.context["answers_list_obj"]
        else:
            answers_list_obj = value.answers.all().order_by("id")

        return AnswerViewSerializer(answers_list_obj, many=True).data


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "question_id",
            # "ans",
        )

    def validate(self, attrs):
        errors = {}
        if "question_id" not in attrs:
            errors.setdefault("question_id", []).append(REQUIRED_FIELD)

        if "ans" not in attrs:
            errors.setdefault("ans", []).append(REQUIRED_FIELD)

        if "question_id" in attrs and attrs["question_id"] is not None:
            if self.context["surveyObj"].id != attrs["question_id"].survey_id.id:
                errors.setdefault("question_id", []).append(
                    INVALID_SURVEY_QUESTION_ID.format(attrs["question_id"].id)
                )

            # elif "ans" in attrs:
            #     if (
            #         attrs["question_id"].is_required
            #         and "ans" in attrs
            #         and attrs["ans"] == ""
            #     ):
            #         errors.setdefault("ans", []).append(NOT_ALLOW_BLANK_VALUE)

            #     elif (
            #         attrs["question_id"].field_type == "N"
            #         and attrs["ans"]
            #         and not attrs["ans"].isdigit()
            #     ):
            #         errors.setdefault("ans", []).append(INVALID_ANS_NUMBER_VALUE)
        if errors:
            raise ValidationError(errors)

        return attrs


class SurveyQuestionAnswerSubmitSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(
        many=True, read_only=False, allow_null=False, required=True
    )

    class Meta:
        model = Answer
        fields = (
            "answers",
            # "invitation_id",
        )

    def validate(self, attrs):
        errors = {}

        # if (
        #     "invitation_id" in attrs
        #     and attrs["invitation_id"] is not None
        #     and self.context["surveyObj"].id != attrs["invitation_id"].survey_id.id
        # ):
        #     errors.setdefault("invitation_id", []).append(
        #         INVALID_SURVEY_INVITATION_ID.format(attrs["invitation_id"].id)
        #     )

        if errors:
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data):
        # invitation_id = validated_data.pop("invitation_id", None)
        ans_uuid = str(uuid.uuid4().hex)

        for ans_data_obj in validated_data["answers"]:
            # ans_data_obj["invitation_id"] = invitation_id
            ans_data_obj["uuid"] = ans_uuid
            ans_data_obj["survey_id"] = self.context["surveyObj"]

            # add survey answer
            Answer.objects.create(**ans_data_obj)

        return ans_uuid
