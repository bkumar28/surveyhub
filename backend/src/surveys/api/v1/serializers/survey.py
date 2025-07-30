import logging

from core.api_message import (
    INVALID_SURVEY_EXPIRED_DATE,
    INVALID_SURVEY_EXPIRED_FUTURE_DATE,
    INVALID_SURVEY_START_DATE,
    QUESTION_MAX_LIMIT,
    START_DATE_MUST_LESS_THAN_EXPIRED_DATE,
)
from django.db.models import Count, Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from surveys.api.v1.serializers.question import (
    QuestionCreateSerializer,
    QuestionCreateUpdateDeleteSerializer,
    QuestionViewSerializer,
)
from surveys.models.answer import Answer
from surveys.models.question import Question
from surveys.models.survey import Survey, SurveyResponse

logger = logging.getLogger(__name__)


# Basic SurveyResponseSerializer for DRF ViewSet usage
class SurveyResponseSerializer(serializers.ModelSerializer):
    answers = serializers.ListField(write_only=True, required=True)

    class Meta:
        model = SurveyResponse
        fields = [
            "id",
            "survey",
            "user",
            "is_complete",
            "started_at",
            "completed_at",
            "answers",
        ]
        read_only_fields = ["id", "user", "started_at", "completed_at"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        request = self.context.get("request")

        # Get survey from URL if not explicitly provided
        if (
            "survey" not in validated_data
            and "view" in self.context
            and "survey_pk" in self.context.get("view").kwargs
        ):
            survey_pk = self.context.get("view").kwargs.get("survey_pk")
            try:
                validated_data["survey"] = Survey.objects.get(pk=survey_pk)
            except Survey.DoesNotExist as err:
                raise serializers.ValidationError(
                    {"survey": f"Survey with ID {survey_pk} does not exist"}
                ) from err

        # Set user if authenticated, otherwise leave as None for anonymous
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user

        # Create the survey response
        survey_response = SurveyResponse.objects.create(**validated_data)

        # Process the answers
        for answer_data in answers_data:
            question_id = answer_data.get("question")
            try:
                question = Question.objects.get(pk=question_id)
                Answer.objects.create(
                    response=survey_response,
                    question=question,
                    text_answer=answer_data.get("text_answer", ""),
                )
            except Question.DoesNotExist:
                # Skip invalid questions
                pass

        return survey_response


class SurveyReportSerializer(serializers.ModelSerializer):
    reports = serializers.SerializerMethodField("get_reports")

    class Meta:
        model = Survey
        fields = (
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
            "reports",
        )
        read_only_fields = fields

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_reports(self, value):
        # get all survey answer
        answers = value.answers.all()

        # get top popular answer object
        popular_answer = (
            answers.filter(~Q(ans=""))
            .values("question_id__title")
            .annotate(total=Count("question_id"))
            .order_by("-total")[:1]
        )

        # get top unpopular answer object
        unpopular_answer = (
            answers.filter(ans="")
            .values("question_id__title")
            .annotate(total=Count("question_id"))
            .order_by("-total")[:1]
        )

        data = {
            "total_submission": answers.values("uuid").distinct().count(),
            "anonymous_user": answers.filter(invitation_id__isnull=True)
            .values("uuid")
            .distinct()
            .count(),
            "invited_user": answers.filter(invitation_id__isnull=False)
            .values("uuid")
            .distinct()
            .count(),
            "total_answer": answers.filter(~Q(ans="")).count(),
            "total_unanswer": answers.filter(ans="").count(),
            "popular_answer": {"total": 0, "question": ""},
            "unpopular_answer": {"total": 0, "question": ""},
        }

        if popular_answer:
            data["popular_answer"]["total"] = popular_answer[0]["total"]
            data["popular_answer"]["question"] = popular_answer[0]["question_id__title"]

        if unpopular_answer:
            data["unpopular_answer"]["total"] = unpopular_answer[0]["total"]
            data["unpopular_answer"]["question"] = unpopular_answer[0][
                "question_id__title"
            ]

        return data


class SurveyViewSerializer(serializers.ModelSerializer):
    questions = QuestionViewSerializer(many=True)

    class Meta:
        model = Survey
        fields = (
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "visibility",
            "is_anonymous",
            "is_public",
            "max_responses",
            "requires_login",
            "allow_multiple_responses",
            "show_progress_bar",
            "thank_you_message",
            "theme_color",
            "logo",
            "custom_css",
            "response_count",
            "completion_rate",
            "average_time",
            "questions",
        )
        read_only_fields = fields


class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = QuestionCreateSerializer(
        many=True, read_only=False, allow_null=False, required=False
    )

    class Meta:
        model = Survey
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
            "questions",
        )

    def validate(self, attrs):
        errors = {}

        if "questions" in attrs and len(attrs["questions"]) > 10:
            errors.setdefault("questions", []).append(QUESTION_MAX_LIMIT)

        if (
            "start_date" in attrs
            and attrs["start_date"] is not None
            and attrs["start_date"] <= timezone.now()
        ):
            errors.setdefault("start_date", []).append(INVALID_SURVEY_START_DATE)

        if (
            "end_date" in attrs
            and attrs["end_date"] is not None
            and attrs["end_date"] < timezone.now()
        ):
            errors.setdefault("end_date", []).append(INVALID_SURVEY_EXPIRED_FUTURE_DATE)

        if (
            "start_date" in attrs
            and attrs.get("end_date") is not None
            and attrs["start_date"] is not None
        ):
            if attrs["end_date"] <= attrs["start_date"]:
                errors.setdefault("end_date", []).append(INVALID_SURVEY_EXPIRED_DATE)

        if errors:
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data):
        # Allow test code to pass created_by directly
        if "created_by" in validated_data:
            user = validated_data.pop("created_by")
        else:
            request = self.context.get("request")
            if (
                not request
                or not hasattr(request, "user")
                or not request.user.is_authenticated
            ):
                raise ValidationError(
                    {
                        "created_by": "This field is required and you must be authenticated."
                    }
                )
            user = request.user
        validated_data["created_by"] = user
        questions = validated_data.pop("questions", [])
        instance = Survey.objects.create(**validated_data)
        if questions:
            self.fields["questions"].create_question(questions, instance)
        return instance


class SurveyUpdateSerializer(serializers.ModelSerializer):
    questions = QuestionCreateUpdateDeleteSerializer(
        many=True, read_only=False, allow_null=False, required=False
    )

    class Meta:
        model = Survey
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
            "questions",
        )

    def validate_questions(self, values):
        if values and "surveyObj" in self.context:
            # get all survey questions
            question_count = self.context["surveyObj"].questions.all().count()

            for xx in values:
                if xx["action_type"] == "POST":
                    question_count += 1
                elif xx["action_type"] == "DELETE":
                    question_count -= 1

            if question_count > 10:
                raise ValidationError(QUESTION_MAX_LIMIT)

        return values

    def validate(self, attrs):
        errors = {}

        if (
            "start_date" in attrs
            and attrs["start_date"] is not None
            and attrs["start_date"] <= timezone.now()
        ):
            errors.setdefault("start_date", []).append(INVALID_SURVEY_START_DATE)

        if "end_date" in attrs and attrs["end_date"] is not None:
            # validate expired date
            if (
                "start_date" not in attrs
                and self.context["surveyObj"].start_date >= attrs["end_date"]
            ):
                errors.setdefault("end_date", []).append(
                    INVALID_SURVEY_EXPIRED_FUTURE_DATE
                )

        if "start_date" in attrs and attrs["start_date"] is not None:
            # validate start date
            if (
                "end_date" not in attrs
                and self.context["surveyObj"].end_date <= attrs["start_date"]
            ):
                errors.setdefault("start_date", []).append(
                    START_DATE_MUST_LESS_THAN_EXPIRED_DATE
                )

            elif (
                "end_date" in attrs
                and attrs["end_date"] is not None
                and attrs["end_date"] <= attrs["start_date"]
            ):
                errors.setdefault("end_date", []).append(INVALID_SURVEY_EXPIRED_DATE)

        if "status" in attrs and attrs["status"] == "S":
            if (
                "start_date" not in attrs
                and self.context["surveyObj"].start_date <= timezone.now()
            ):
                errors.setdefault("start_date", []).append(INVALID_SURVEY_START_DATE)

            if (
                "end_date" not in attrs
                and self.context["surveyObj"].end_date <= timezone.now()
            ):
                errors.setdefault("end_date", []).append(
                    INVALID_SURVEY_EXPIRED_FUTURE_DATE
                )

        if errors:
            raise ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):
        questions = validated_data.pop("questions", [])

        if validated_data:
            # set survey fields value
            for key, item in validated_data.items():
                setattr(instance, key, item)

            instance.updated_on = timezone.now()

            # update survey
            instance.save()

        if questions:
            # add/update/delete survey questions
            self.fields["questions"].batch_question_func(questions, instance)

        return instance
