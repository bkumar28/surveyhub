import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from surveys.models.survey import Survey, SurveyStatus, SurveyVisibility


@pytest.mark.django_db
def test_create_survey():
    user_model = get_user_model()
    user = user_model.objects.create_user(username="testuser", password="testpass")
    survey = Survey.objects.create(
        title="Test Survey",
        description="A test survey.",
        created_by=user,
        status=SurveyStatus.DRAFT,
        visibility=SurveyVisibility.PUBLIC,
        start_date=timezone.now(),
    )
    assert survey.title == "Test Survey"
    assert survey.status == SurveyStatus.DRAFT
    assert survey.visibility == SurveyVisibility.PUBLIC
    assert survey.created_by == user
    assert survey.is_anonymous is True
    assert survey.is_active is False


@pytest.mark.django_db
def test_survey_is_active():
    user_model = get_user_model()
    user = user_model.objects.create_user(username="activeuser", password="testpass")
    now = timezone.now()
    survey = Survey.objects.create(
        title="Active Survey",
        description="Active test survey.",
        created_by=user,
        status=SurveyStatus.ACTIVE,
        visibility=SurveyVisibility.PUBLIC,
        start_date=now,
        end_date=now + timezone.timedelta(days=1),
    )
    assert survey.is_active is True


@pytest.mark.django_db
def test_survey_response_limit_reached():
    user_model = get_user_model()
    user = user_model.objects.create_user(username="limituser", password="testpass")
    survey = Survey.objects.create(
        title="Limited Survey",
        description="Limited test survey.",
        created_by=user,
        max_responses=5,
        response_count=5,
    )
    assert survey.response_limit_reached is True
