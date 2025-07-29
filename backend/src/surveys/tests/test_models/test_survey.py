import uuid
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from surveys.models.survey import SurveyStatus, SurveyVisibility
from surveys.tests.factories.survey_factory import (
    SurveyFactory,
    SurveyResponseFactory,
    UserFactory,
)


class SurveyModelTest(TestCase):
    """Test cases for Survey model"""

    def setUp(self):
        self.user = UserFactory()
        self.survey = SurveyFactory(created_by=self.user)
        self.response = SurveyResponseFactory(survey=self.survey, user=self.user)

    def test_survey_creation(self):
        survey = SurveyFactory(
            created_by=self.user,
            title="Test Survey",
            status=SurveyStatus.DRAFT,
            visibility=SurveyVisibility.PUBLIC,
            is_anonymous=True,
            is_public=True,
            max_responses=100,
            requires_login=False,
            allow_multiple_responses=False,
            show_progress_bar=True,
            thank_you_message="Thank you for your response!",
            theme_color="#007bff",
            response_count=0,
            completion_rate=0.0,
            average_time=None,
        )
        self.assertEqual(survey.title, "Test Survey")
        self.assertEqual(survey.created_by, self.user)
        self.assertEqual(survey.status, SurveyStatus.DRAFT)
        self.assertEqual(survey.visibility, SurveyVisibility.PUBLIC)
        self.assertTrue(survey.is_anonymous)
        self.assertTrue(survey.is_public)
        self.assertEqual(survey.max_responses, 100)
        self.assertFalse(survey.requires_login)
        self.assertFalse(survey.allow_multiple_responses)
        self.assertTrue(survey.show_progress_bar)
        self.assertEqual(survey.thank_you_message, "Thank you for your response!")
        self.assertEqual(survey.theme_color, "#007bff")
        self.assertEqual(survey.response_count, 0)
        self.assertEqual(survey.completion_rate, 0.0)
        self.assertIsNone(survey.average_time)
        self.assertIsInstance(survey.id, uuid.UUID)

    def test_survey_str_method(self):
        survey = SurveyFactory(title="Test Survey", created_by=self.user)
        self.assertEqual(str(survey), "Test Survey")

    def test_survey_is_active_property(self):
        # Active survey within time window
        survey = SurveyFactory(
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            start_date=timezone.now() - timedelta(hours=1),
            end_date=timezone.now() + timedelta(hours=1),
        )
        self.assertTrue(survey.is_active)

        # Inactive survey (wrong status)
        survey = SurveyFactory(
            created_by=self.user,
            status=SurveyStatus.DRAFT,
            start_date=timezone.now() - timedelta(hours=1),
            end_date=timezone.now() + timedelta(hours=1),
        )
        self.assertFalse(survey.is_active)

        # Inactive survey (before start date)
        survey = SurveyFactory(
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            start_date=timezone.now() + timedelta(hours=1),
            end_date=timezone.now() + timedelta(hours=2),
        )
        self.assertFalse(survey.is_active)

        # Inactive survey (after end date)
        survey = SurveyFactory(
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            start_date=timezone.now() - timedelta(hours=2),
            end_date=timezone.now() - timedelta(hours=1),
        )
        self.assertFalse(survey.is_active)

    def test_response_limit_reached_property(self):
        # Without max_responses
        survey = SurveyFactory(
            created_by=self.user, max_responses=None, response_count=0
        )
        self.assertFalse(survey.response_limit_reached)

        # With max_responses not reached
        survey = SurveyFactory(created_by=self.user, max_responses=10, response_count=5)
        self.assertFalse(survey.response_limit_reached)

        # With max_responses reached
        survey = SurveyFactory(
            created_by=self.user, max_responses=10, response_count=10
        )
        self.assertTrue(survey.response_limit_reached)

        # With max_responses exceeded
        survey = SurveyFactory(
            created_by=self.user, max_responses=10, response_count=15
        )
        self.assertTrue(survey.response_limit_reached)

    def test_survey_ordering(self):
        survey1 = SurveyFactory(created_by=self.user, title="First Survey")
        survey2 = SurveyFactory(created_by=self.user, title="Second Survey")
        surveys = list(type(survey1).objects.all())
        self.assertEqual(surveys[0], survey2)  # Most recent first
        self.assertEqual(surveys[1], survey1)


class SurveyResponseModelTest(TestCase):
    """Test cases for SurveyResponse model"""

    def setUp(self):
        self.user = UserFactory()
        self.survey = SurveyFactory(created_by=self.user)

    def test_survey_response_creation(self):
        response = SurveyResponseFactory(
            survey=self.survey,
            user=self.user,
            ip_address="127.0.0.1",
            user_agent="Test Browser",
            referrer="https://example.com",
            is_complete=False,
            country="US",
            city="New York",
        )
        self.assertEqual(response.survey, self.survey)
        self.assertEqual(response.user, self.user)
        self.assertEqual(response.ip_address, "127.0.0.1")
        self.assertEqual(response.user_agent, "Test Browser")
        self.assertEqual(response.referrer, "https://example.com")
        self.assertFalse(response.is_complete)
        self.assertEqual(response.country, "US")
        self.assertEqual(response.city, "New York")
        self.assertIsInstance(response.user_token, uuid.UUID)

    def test_survey_response_str_method(self):
        response = SurveyResponseFactory(survey=self.survey, user=self.user)
        expected = f"Response to {self.survey.title} by {self.user}"
        self.assertEqual(str(response), expected)

    def test_anonymous_survey_response(self):
        response = SurveyResponseFactory(
            survey=self.survey, user=None, session_key="test-session-key"
        )
        self.assertIsNone(response.user)
        self.assertEqual(response.session_key, "test-session-key")
        expected = f"Response to {self.survey.title} by Anonymous"
        self.assertEqual(str(response), expected)
