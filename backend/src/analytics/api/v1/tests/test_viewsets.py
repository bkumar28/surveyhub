from analytics.tests.factories import QuestionAnalyticsFactory, SurveyAnalyticsFactory
from django.urls import reverse
from rest_framework.test import APITestCase
from surveys.tests.factories.question_factory import QuestionFactory
from surveys.tests.factories.survey_factory import SurveyFactory


class SurveyAnalyticsViewSetTest(APITestCase):
    def setUp(self):
        self.survey = SurveyFactory()
        self.analytics = SurveyAnalyticsFactory(survey=self.survey)
        self.list_url = reverse("analytics:survey-analytics-list")
        self.detail_url = reverse(
            "analytics:survey-analytics-detail", args=[self.analytics.id]
        )

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        # Use custom pagination structure
        self.assertIn("data", response.data)
        self.assertIn("results", response.data["data"])
        self.assertTrue(
            any(
                item["id"] == str(self.analytics.id)
                for item in response.data["data"]["results"]
            )
        )

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.data["id"]), str(self.analytics.id))


class QuestionAnalyticsViewSetTest(APITestCase):
    def setUp(self):
        self.question = QuestionFactory()
        self.analytics = QuestionAnalyticsFactory(question=self.question)
        self.list_url = reverse("analytics:question-analytics-list")
        self.detail_url = reverse(
            "analytics:question-analytics-detail", args=[self.analytics.id]
        )

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.data)
        self.assertIn("results", response.data["data"])
        self.assertTrue(
            any(
                item["id"] == str(self.analytics.id)
                for item in response.data["data"]["results"]
            )
        )

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.data["id"]), str(self.analytics.id))
