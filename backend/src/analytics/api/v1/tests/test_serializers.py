from analytics.api.v1.serializers import (
    QuestionAnalyticsSerializer,
    SurveyAnalyticsSerializer,
)
from analytics.tests.factories import QuestionAnalyticsFactory, SurveyAnalyticsFactory
from django.test import TestCase


class SurveyAnalyticsSerializerTest(TestCase):
    def setUp(self):
        self.analytics = SurveyAnalyticsFactory()

    def test_serialized_data(self):
        serializer = SurveyAnalyticsSerializer(instance=self.analytics)
        self.assertEqual(serializer.data["total_views"], self.analytics.total_views)
        self.assertEqual(
            serializer.data["total_completions"], self.analytics.total_completions
        )


class QuestionAnalyticsSerializerTest(TestCase):
    def setUp(self):
        self.analytics = QuestionAnalyticsFactory()

    def test_serialized_data(self):
        serializer = QuestionAnalyticsSerializer(instance=self.analytics)
        self.assertEqual(serializer.data["total_answers"], self.analytics.total_answers)
        self.assertEqual(serializer.data["skip_count"], self.analytics.skip_count)
