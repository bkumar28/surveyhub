from blueprints.tests.factories import (
    BlueprintCategoryFactory,
    QuestionBlueprintFactory,
    SurveyBlueprintFactory,
    UserFactory,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BlueprintCategoryViewsTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", email="test@example.com")
        self.category = BlueprintCategoryFactory(
            name="Customer Feedback", description="Feedback forms", order=1
        )

    def test_list_categories(self):
        url = reverse("blueprints:blueprintcategory-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_category_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("blueprints:blueprintcategory-list")
        data = {
            "name": "Employee Feedback",
            "description": "Employee forms",
            "order": 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Employee Feedback")


class SurveyBlueprintViewsTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser2", email="test2@example.com")
        self.category = BlueprintCategoryFactory(
            name="Market Research", description="Market forms", order=1
        )
        self.survey_blueprint = SurveyBlueprintFactory(
            name="Market Survey",
            description="A survey for market research",
            category=self.category,
            tags=["market", "research"],
            is_public=True,
            created_by=self.user,
            blueprint_data={"title": "Market Survey", "questions": []},
        )

    def test_list_survey_blueprints(self):
        url = reverse("blueprints:surveyblueprint-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_survey_blueprint_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("blueprints:surveyblueprint-list")
        data = {
            "name": "Employee Survey",
            "description": "A survey for employees",
            "category": str(self.category.id),
            "tags": ["employee"],
            "is_public": True,
            "blueprint_data": {"title": "Employee Survey", "questions": []},
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Employee Survey")


class QuestionBlueprintViewsTest(APITestCase):
    def setUp(self):
        self.category = BlueprintCategoryFactory(
            name="General", description="General questions", order=1
        )
        self.question_blueprint = QuestionBlueprintFactory(
            title="Satisfaction Rating",
            field_type="R",
            category="general",
            blueprint_data={"field_type": "R", "scale_min": 1, "scale_max": 5},
        )

    def test_list_question_blueprints(self):
        url = reverse("blueprints:questionblueprint-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_question_blueprint_authenticated(self):
        user = UserFactory(username="testuser3", email="test3@example.com")
        self.client.force_authenticate(user=user)
        url = reverse("blueprints:questionblueprint-list")
        data = {
            "title": "Net Promoter Score",
            "field_type": "S",
            "category": "nps",
            "blueprint_data": {"field_type": "S", "scale_min": 0, "scale_max": 10},
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Net Promoter Score")
