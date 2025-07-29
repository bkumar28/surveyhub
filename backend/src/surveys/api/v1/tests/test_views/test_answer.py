from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from surveys.models.question import FieldType, Question
from surveys.models.survey import Survey, SurveyResponse

User = get_user_model()


class QuestionViewsTest(APITestCase):
    """Test cases for Question API views"""

    def setUp(self):
        """Set up test data"""
        # Clear all existing data to prevent test pollution
        Survey.objects.all().delete()
        Question.objects.all().delete()
        SurveyResponse.objects.all().delete()

        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.survey = Survey.objects.create(
            title="Test Survey",
            description="A test survey",
            created_by=self.user,
            start_date=timezone.now(),
        )

        self.question = Question.objects.create(
            survey=self.survey,
            title="Test Question",
            description="A test question",
            field_type=FieldType.TEXT,
            is_required=True,
            order=1,
        )

    def test_get_question_list(self):
        """Test getting list of questions for a survey"""
        url = reverse("surveys:question-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # With custom pagination, data is nested inside response.data['data']['results']
        results = response.data.get("data", {}).get("results", [])
        # Check that we have at least one question
        self.assertGreaterEqual(len(results), 1)
        # Find our test question in the results
        found_test_question = False
        for question in results:
            if question["title"] == "Test Question":
                found_test_question = True
                break
        self.assertTrue(found_test_question, "Test question not found in results")

    def test_get_question_detail(self):
        """Test getting question detail"""
        url = reverse(
            "surveys:question-detail",
            kwargs={"survey_pk": self.survey.pk, "pk": self.question.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], "Test Question")
        self.assertEqual(response.data["data"]["field_type"], FieldType.TEXT)

    def test_create_question_authenticated(self):
        """Test creating question with authentication"""
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "New Question",
            "description": "A new question description",
            "field_type": FieldType.SINGLE_CHOICE,
            "is_required": False,
            "order": 2,
            "options": ["Option 1", "Option 2", "Option 3"],
        }

        url = reverse("surveys:question-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["title"], "New Question")
        self.assertEqual(response.data["data"]["field_type"], FieldType.SINGLE_CHOICE)
        self.assertEqual(
            response.data["data"]["options"], ["Option 1", "Option 2", "Option 3"]
        )

    def test_create_question_unauthenticated(self):
        """Test creating question without authentication"""
        data = {
            "title": "New Question",
            "field_type": FieldType.TEXT,
            "order": 2,
        }

        url = reverse("surveys:question-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_question_owner(self):
        """Test updating question by survey owner"""
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Updated Question Title",
            "description": "Updated description",
            "is_required": False,
        }

        url = reverse(
            "surveys:question-detail",
            kwargs={"survey_pk": self.survey.pk, "pk": self.question.pk},
        )
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], "Updated Question Title")
        self.assertEqual(response.data["data"]["description"], "Updated description")
        self.assertFalse(response.data["data"]["is_required"])

    def test_delete_question_owner(self):
        """Test deleting question by survey owner"""
        self.client.force_authenticate(user=self.user)

        url = reverse(
            "surveys:question-detail",
            kwargs={"survey_pk": self.survey.pk, "pk": self.question.pk},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())

    def test_question_ordering(self):
        """Test question ordering"""
        self.client.force_authenticate(user=self.user)

        # Create second question
        Question.objects.create(
            survey=self.survey,
            title="Second Question",
            field_type=FieldType.NUMBER,
            order=2,
        )

        url = reverse("surveys:question-list", kwargs={"survey_pk": self.survey.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # With custom pagination, data is nested inside response.data['data']['results']
        results = response.data.get("data", {}).get("results", [])

        # Check that both questions exist in results (may include others)
        first_question_found = False
        second_question_found = False

        for question in results:
            if question["title"] == "Test Question" and question["order"] == 1:
                first_question_found = True
            elif question["title"] == "Second Question" and question["order"] == 2:
                second_question_found = True

        self.assertTrue(
            first_question_found, "First question not found or has wrong order"
        )
        self.assertTrue(
            second_question_found, "Second question not found or has wrong order"
        )
