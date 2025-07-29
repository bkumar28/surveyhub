from django.test import TestCase

from .factories import QuestionAnalyticsFactory, SurveyAnalyticsFactory


class SurveyAnalyticsModelTest(TestCase):
    def test_str(self):
        analytics = SurveyAnalyticsFactory()
        self.assertIn("Analytics for", str(analytics))


class QuestionAnalyticsModelTest(TestCase):
    def test_str(self):
        analytics = QuestionAnalyticsFactory()
        self.assertIn("Analytics for", str(analytics))
