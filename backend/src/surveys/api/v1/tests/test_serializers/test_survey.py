import uuid

import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from surveys.api.v1.serializers.survey import (
    SurveyCreateSerializer,
    SurveyUpdateSerializer,
    SurveyViewSerializer,
)
from surveys.tests.factories.survey_factory import SurveyFactory, UserFactory


@pytest.mark.django_db
class TestSurveyCreateSerializer:
    def test_valid_survey_creation(self):
        user = UserFactory()
        payload = {
            "title": "Survey A",
            "description": "Description",
            "start_date": timezone.now() + timezone.timedelta(days=1),
            "end_date": timezone.now() + timezone.timedelta(days=5),
            "status": "D",
            "questions": [],
        }
        serializer = SurveyCreateSerializer(data=payload)
        assert serializer.is_valid(), serializer.errors
        survey = serializer.save(created_by=user)
        assert survey.title == payload["title"]
        assert survey.created_by == user

    def test_question_limit_exceeded(self):
        payload = {
            "title": "Too many questions",
            "description": "Test limit",
            "start_date": timezone.now() + timezone.timedelta(days=1),
            "end_date": timezone.now() + timezone.timedelta(days=5),
            "status": "D",
            "questions": [{}] * 11,
        }
        serializer = SurveyCreateSerializer(data=payload)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "questions" in str(excinfo.value)

    def test_invalid_start_and_end_dates(self):
        now = timezone.now()
        payload = {
            "title": "Invalid Dates",
            "description": "Test",
            "start_date": now - timezone.timedelta(days=1),
            "end_date": now - timezone.timedelta(days=2),
            "status": "D",
            "questions": [],
        }
        serializer = SurveyCreateSerializer(data=payload)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "start_date" in str(excinfo.value)
        assert "end_date" in str(excinfo.value)


@pytest.mark.django_db
class TestSurveyUpdateSerializer:
    def test_update_questions_exceed_limit(self):
        survey = SurveyFactory()
        questions = [{"action_type": "POST"} for _ in range(11)]
        serializer = SurveyUpdateSerializer(
            instance=survey,
            data={"questions": questions},
            context={"surveyObj": survey},
            partial=True,
        )
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "questions" in str(excinfo.value)

    def test_invalid_end_date_before_start(self):
        survey = SurveyFactory(
            start_date=timezone.now() + timezone.timedelta(days=5),
            end_date=timezone.now() + timezone.timedelta(days=10),
        )
        data = {
            "start_date": timezone.now() + timezone.timedelta(days=15),
            "end_date": timezone.now() + timezone.timedelta(days=12),
        }
        serializer = SurveyUpdateSerializer(
            instance=survey,
            data=data,
            context={"surveyObj": survey},
            partial=True,
        )
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "end_date" in str(excinfo.value)


@pytest.mark.django_db
class TestSurveyViewSerializer:
    def test_view_serializer_output(self):
        survey = SurveyFactory(id=uuid.uuid4())
        serializer = SurveyViewSerializer(instance=survey)
        data = serializer.data
        assert data["id"] == str(survey.id)
        assert "questions" in data
