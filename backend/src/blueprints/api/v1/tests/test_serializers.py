from blueprints.api.v1.serializers.blueprint import (
    QuestionBlueprintSerializer,
    SurveyBlueprintSerializer,
)
from blueprints.api.v1.serializers.category import (
    BlueprintCategorySerializer,
)
from blueprints.tests.factories import (
    BlueprintCategoryFactory,
    QuestionBlueprintFactory,
    SurveyBlueprintFactory,
)
from core.factories import UserFactory
from django.test import TestCase


class BlueprintCategorySerializerTest(TestCase):
    def test_serializer(self):
        category = BlueprintCategoryFactory(
            name="Customer Feedback", description="Feedback forms", order=1
        )
        serializer = BlueprintCategorySerializer(category)
        data = serializer.data
        self.assertEqual(data["name"], "Customer Feedback")
        self.assertEqual(data["description"], "Feedback forms")
        self.assertEqual(data["order"], 1)


class SurveyBlueprintSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser2", email="test2@example.com")
        self.category = BlueprintCategoryFactory(
            name="Market Research", description="Market forms", order=1
        )

    def test_serializer(self):
        survey = SurveyBlueprintFactory(
            name="Market Survey",
            description="A survey for market research",
            category=self.category,
            tags=["market", "research"],
            is_public=True,
            created_by=self.user,
            blueprint_data={"title": "Market Survey", "questions": []},
        )
        serializer = SurveyBlueprintSerializer(survey)
        data = serializer.data
        self.assertEqual(data["name"], "Market Survey")
        self.assertEqual(data["category"], self.category.id)
        self.assertEqual(data["is_public"], True)
        self.assertEqual(data["created_by"], self.user.username)
        self.assertEqual(
            data["blueprint_data"], {"title": "Market Survey", "questions": []}
        )


class QuestionBlueprintSerializerTest(TestCase):
    def test_serializer(self):
        qb = QuestionBlueprintFactory(
            title="Satisfaction Rating",
            field_type="R",
            category="general",
            blueprint_data={"field_type": "R", "scale_min": 1, "scale_max": 5},
        )
        serializer = QuestionBlueprintSerializer(qb)
        data = serializer.data
        self.assertEqual(data["title"], "Satisfaction Rating")
        self.assertEqual(data["field_type"], "R")
        self.assertEqual(data["category"], "general")
        self.assertEqual(
            data["blueprint_data"], {"field_type": "R", "scale_min": 1, "scale_max": 5}
        )
