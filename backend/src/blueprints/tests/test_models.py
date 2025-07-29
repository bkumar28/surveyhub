from core.factories import UserFactory
from django.test import TestCase

from .factories import (
    BlueprintCategoryFactory,
    QuestionBlueprintFactory,
    SurveyBlueprintFactory,
)


class BlueprintCategoryModelTest(TestCase):
    def test_create_category(self):
        category = BlueprintCategoryFactory(
            name="Customer Feedback", description="Feedback forms", order=1
        )
        self.assertEqual(str(category), "Customer Feedback")
        self.assertEqual(category.description, "Feedback forms")
        self.assertEqual(category.order, 1)


class SurveyBlueprintModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", email="test@example.com")
        self.category = BlueprintCategoryFactory(
            name="Market Research", description="Market forms", order=1
        )

    def test_create_survey_blueprint(self):
        survey = SurveyBlueprintFactory(
            name="Market Survey",
            description="A survey for market research",
            category=self.category,
            tags=["market", "research"],
            is_public=True,
            created_by=self.user,
            blueprint_data={"title": "Market Survey", "questions": []},
        )
        self.assertEqual(str(survey), "Market Survey")
        self.assertEqual(survey.category, self.category)
        self.assertTrue(survey.is_public)
        self.assertEqual(survey.created_by, self.user)


class QuestionBlueprintModelTest(TestCase):
    def test_create_question_blueprint(self):
        qb = QuestionBlueprintFactory(
            title="Satisfaction Rating",
            field_type="R",
            category="general",
            blueprint_data={"field_type": "R", "scale_min": 1, "scale_max": 5},
        )
        self.assertEqual(str(qb), "Satisfaction Rating")
        self.assertEqual(qb.field_type, "R")
        self.assertEqual(qb.category, "general")
