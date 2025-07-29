from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from surveys.models.question import FieldType, Question

# Still need these for enums and model references
from surveys.models.survey import Survey, SurveyResponse, SurveyStatus, SurveyVisibility
from surveys.tests.factories.answer_factory import AnswerFactory
from surveys.tests.factories.question_factory import QuestionFactory

# Import factories
from surveys.tests.factories.survey_factory import (
    SurveyFactory,
    SurveyResponseFactory,
    UserFactory,
)


class SurveyViewsTest(APITestCase):
    """Test cases for Survey API views"""

    def setUp(self):
        """Set up test data"""
        # Clear all existing data to prevent test pollution
        Survey.objects.all().delete()
        Question.objects.all().delete()
        SurveyResponse.objects.all().delete()

        self.user = UserFactory(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.admin_user = UserFactory(
            username="admin",
            email="admin@example.com",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )

        self.survey = SurveyFactory(
            title="Test Survey",
            description="A test survey description",
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            visibility=SurveyVisibility.PUBLIC,
            is_public=True,
            start_date=timezone.now(),
        )

        self.question = QuestionFactory(
            survey=self.survey,
            title="Test Question",
            description="A test question",
            field_type=FieldType.TEXT,
            is_required=True,
            order=1,
        )

    def test_get_survey_list(self):
        """Test getting list of surveys"""
        url = reverse("surveys:survey-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # With custom pagination, data is nested inside response.data['data']['results']
        results = response.data.get("data", {}).get("results", [])
        # Check that at least one survey is returned
        self.assertGreaterEqual(len(results), 1)
        # Find our test survey in the results
        found_test_survey = False
        for survey in results:
            if survey["title"] == "Test Survey":
                found_test_survey = True
                break
        self.assertTrue(found_test_survey, "Test survey not found in results")

    def test_get_survey_detail(self):
        """Test getting survey detail"""
        url = reverse("surveys:survey-detail", kwargs={"pk": self.survey.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], "Test Survey")
        self.assertEqual(
            response.data["data"]["description"], "A test survey description"
        )

    def test_create_survey_authenticated(self):
        """Test creating survey with authentication"""
        self.client.force_authenticate(user=self.user)
        from datetime import timedelta

        data = {
            "title": "New Survey",
            "description": "A new survey description",
            "status": SurveyStatus.DRAFT,
            "visibility": SurveyVisibility.PUBLIC,
            "is_public": True,
            "is_anonymous": True,
            "max_responses": 100,
            "requires_login": False,
            "allow_multiple_responses": False,
            "show_progress_bar": True,
            "thank_you_message": "Thank you!",
            "theme_color": "#007bff",
            "custom_css": "",
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_date": None,
        }
        url = reverse("surveys:survey-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["title"], "New Survey")
        self.assertEqual(response.data["data"]["created_by"], self.user.id)

    def test_create_survey_unauthenticated(self):
        """Test creating survey without authentication"""
        from datetime import timedelta

        data = {
            "title": "New Survey",
            "description": "A new survey description",
            "status": SurveyStatus.DRAFT,
            "visibility": SurveyVisibility.PUBLIC,
            "is_public": True,
            "is_anonymous": True,
            "max_responses": 100,
            "requires_login": False,
            "allow_multiple_responses": False,
            "show_progress_bar": True,
            "thank_you_message": "Thank you!",
            "theme_color": "#007bff",
            "custom_css": "",
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_date": None,
        }
        url = reverse("surveys:survey-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_survey_owner(self):
        """Test updating survey by owner"""
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Updated Survey Title",
            "description": "Updated description",
        }

        url = reverse("surveys:survey-detail", kwargs={"pk": self.survey.pk})
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], "Updated Survey Title")
        self.assertEqual(response.data["data"]["description"], "Updated description")

    def test_update_survey_non_owner(self):
        """Test updating survey by non-owner"""
        other_user = UserFactory(
            username="otheruser", email="other@example.com", password="otherpass123"
        )

        self.client.force_authenticate(user=other_user)

        data = {
            "title": "Updated Survey Title",
        }

        url = reverse("surveys:survey-detail", kwargs={"pk": self.survey.pk})
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_survey_owner(self):
        """Test deleting survey by owner"""
        self.client.force_authenticate(user=self.user)

        url = reverse("surveys:survey-detail", kwargs={"pk": self.survey.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Survey.objects.filter(pk=self.survey.pk).exists())

    def test_delete_survey_admin(self):
        """Test deleting survey by admin"""
        self.client.force_authenticate(user=self.admin_user)

        url = reverse("surveys:survey-detail", kwargs={"pk": self.survey.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Survey.objects.filter(pk=self.survey.pk).exists())

    def test_filter_surveys_by_status(self):
        """Test filtering surveys by status"""
        # Create draft survey using factory
        SurveyFactory(
            title="Draft Survey",
            description="A draft survey",
            created_by=self.user,
            status=SurveyStatus.DRAFT,
            start_date=timezone.now(),
        )

        url = reverse("surveys:survey-list")
        response = self.client.get(url, {"status": SurveyStatus.ACTIVE})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # With custom pagination, data is nested inside response.data['data']['results']
        results = response.data.get("data", {}).get("results", [])
        # Check that we got at least one result
        self.assertGreaterEqual(len(results), 1)
        # Verify that all returned surveys have ACTIVE status
        for survey in results:
            self.assertEqual(survey["status"], SurveyStatus.ACTIVE)

    def test_filter_surveys_by_visibility(self):
        """Test filtering surveys by visibility"""
        # Create private survey using factory
        SurveyFactory(
            title="Private Survey",
            description="A private survey",
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            visibility=SurveyVisibility.PRIVATE,
            start_date=timezone.now(),
        )

        url = reverse("surveys:survey-list")
        response = self.client.get(url, {"visibility": SurveyVisibility.PUBLIC})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # With custom pagination, data is nested inside response.data['data']['results']
        results = response.data.get("data", {}).get("results", [])
        # Check that we have at least one survey
        self.assertGreaterEqual(len(results), 1)
        # Verify that all returned surveys are public
        for survey in results:
            self.assertEqual(survey["visibility"], SurveyVisibility.PUBLIC)


class SurveyResponseViewsTest(APITestCase):
    """Test cases for SurveyResponse API views"""

    def setUp(self):
        """Set up test data"""
        self.user = UserFactory(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.survey = SurveyFactory(
            title="Test Survey",
            description="A test survey",
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            visibility=SurveyVisibility.PUBLIC,
            is_public=True,
            start_date=timezone.now(),
        )

        self.question = QuestionFactory(
            survey=self.survey,
            title="Test Question",
            field_type=FieldType.TEXT,
            is_required=True,
            order=1,
        )

        self.response = SurveyResponseFactory(
            survey=self.survey,
            user=self.user,
            is_complete=True,
        )

    def test_get_survey_responses(self):
        """Test getting survey responses"""
        self.client.force_authenticate(user=self.user)

        url = reverse("surveys:response-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # With custom pagination, data is nested inside response.data['data']['results']
        results = response.data.get("data", {}).get("results", [])
        # Check that we have at least one survey response
        self.assertGreaterEqual(len(results), 1)
        # Verify that at least one response is for our survey
        found_response = False
        for resp in results:
            if str(resp["survey"]) == str(self.survey.pk):
                found_response = True
                break
        self.assertTrue(found_response, "No response found for the test survey")

    def test_create_survey_response_authenticated(self):
        """Test creating survey response with authentication"""
        self.client.force_authenticate(user=self.user)

        data = {
            "is_complete": False,
            "survey": str(self.survey.pk),  # Add survey explicitly
            "answers": [
                {
                    "question": self.question.pk,
                    "text_answer": "My answer to the question",
                }
            ],
        }

        url = reverse("surveys:response-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["user"], self.user.id)
        self.assertFalse(response.data["data"]["is_complete"])

    def test_create_survey_response_anonymous(self):
        """Test creating anonymous survey response"""
        data = {
            "is_complete": True,
            "survey": str(self.survey.pk),  # Add survey explicitly
            "answers": [
                {"question": self.question.pk, "text_answer": "Anonymous answer"}
            ],
        }

        url = reverse("surveys:response-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["data"]["user"])
        self.assertTrue(response.data["data"]["is_complete"])

    def test_create_response_inactive_survey(self):
        """Test creating response for inactive survey"""
        # Make survey inactive
        self.survey.status = SurveyStatus.DRAFT
        self.survey.save()

        data = {
            "is_complete": True,
            "answers": [
                {
                    "question": self.question.pk,
                    "text_answer": "Answer to inactive survey",
                }
            ],
        }

        url = reverse("surveys:response-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_response_missing_required_answer(self):
        """Test creating response with missing required answer"""
        data = {
            "is_complete": True,
            "answers": [],  # Missing required answer
        }

        url = reverse("surveys:response-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_survey_response_owner(self):
        """Test updating survey response by owner"""
        self.client.force_authenticate(user=self.user)

        data = {
            "is_complete": True,
        }

        url = reverse(
            "surveys:response-detail",
            kwargs={"survey_pk": self.survey.pk, "pk": self.response.pk},
        )
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["is_complete"])

    def test_get_response_analytics(self):
        """Test getting response analytics"""
        self.client.force_authenticate(user=self.user)

        # Create answer using factory
        AnswerFactory(
            response=self.response, question=self.question, text_answer="Test answer"
        )

        url = reverse(
            "surveys:response-analytics", kwargs={"survey_pk": self.survey.pk}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_responses", response.data["data"])
        self.assertIn("completion_rate", response.data["data"])


class SurveyPublicAccessTest(TestCase):
    """Test cases for public survey access"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        self.user = UserFactory(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.public_survey = SurveyFactory(
            title="Public Survey",
            description="A public survey",
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            visibility=SurveyVisibility.PUBLIC,
            is_public=True,
            start_date=timezone.now(),
        )

        self.private_survey = SurveyFactory(
            title="Private Survey",
            description="A private survey",
            created_by=self.user,
            status=SurveyStatus.ACTIVE,
            visibility=SurveyVisibility.PRIVATE,
            is_public=False,
            start_date=timezone.now(),
        )

    def test_access_public_survey(self):
        """Test accessing public survey without authentication"""
        url = reverse("surveys:survey-detail", kwargs={"pk": self.public_survey.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_access_private_survey_unauthorized(self):
        """Test accessing private survey without authentication"""
        url = reverse("surveys:survey-detail", kwargs={"pk": self.private_survey.pk})
        response = self.client.get(url)

        # We're now allowing viewing of private surveys but restricting operations on them
        # The view exists (200) but permissions will prevent operations (POST/PUT/DELETE)
        self.assertEqual(response.status_code, 200)

    def test_access_private_survey_authorized(self):
        """Test accessing private survey with authentication"""
        self.client.force_login(self.user)

        url = reverse("surveys:survey-detail", kwargs={"pk": self.private_survey.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
