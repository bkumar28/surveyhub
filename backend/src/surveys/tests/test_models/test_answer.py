from django.test import TestCase
from django.utils import timezone
from surveys.tests.factories.answer_factory import AnswerFactory
from surveys.tests.factories.question_factory import (
    QuestionFactory,
    QuestionOptionFactory,
)
from surveys.tests.factories.survey_factory import (
    SurveyFactory,
    SurveyResponseFactory,
    UserFactory,
)


class AnswerModelTest(TestCase):
    """Test cases for Answer model"""

    def setUp(self):
        self.user = UserFactory(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.survey = SurveyFactory(created_by=self.user)
        self.question = QuestionFactory(survey=self.survey)
        self.response = SurveyResponseFactory(survey=self.survey, user=self.user)
        self.option = QuestionOptionFactory(question=self.question)

    def test_text_answer_creation(self):
        answer = AnswerFactory(
            response=self.response,
            question=self.question,
            text_answer="This is a text answer",
        )
        self.assertEqual(answer.response, self.response)
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.text_answer, "This is a text answer")
        self.assertEqual(answer.display_value, "This is a text answer")

    def test_number_answer_creation(self):
        answer = AnswerFactory(
            response=self.response,
            question=self.question,
            text_answer="",  # Use empty string instead of None
            number_answer=42.5,
        )
        self.assertEqual(answer.number_answer, 42.5)
        self.assertEqual(answer.display_value, "42.5")

    def test_date_answer_creation(self):
        test_date = timezone.now().date()
        answer = AnswerFactory(
            response=self.response,
            question=self.question,
            text_answer="",  # Use empty string instead of None
            date_answer=test_date,
        )
        self.assertEqual(answer.date_answer, test_date)
        self.assertEqual(answer.display_value, test_date.strftime("%Y-%m-%d"))

    def test_datetime_answer_creation(self):
        test_datetime = timezone.now()
        answer = AnswerFactory(
            response=self.response,
            question=self.question,
            text_answer="",  # Use empty string instead of None
            datetime_answer=test_datetime,
        )
        self.assertEqual(answer.datetime_answer, test_datetime)
        self.assertEqual(answer.display_value, test_datetime.strftime("%Y-%m-%d %H:%M"))

    def test_json_answer_creation(self):
        json_data = {
            "selected_options": ["option1", "option2"],
            "other_text": "custom answer",
        }
        answer = AnswerFactory(
            response=self.response,
            question=self.question,
            text_answer="",  # Use empty string instead of None
            json_answer=json_data,
        )
        self.assertEqual(answer.json_answer, json_data)
        # Check that the display_value contains elements from our JSON
        display_value = answer.display_value
        self.assertTrue(
            "selected_options" in str(display_value)
            or "option1" in str(display_value)
            or "option2" in str(display_value)
        )

    def test_answer_str_method(self):
        answer = AnswerFactory(
            response=self.response, question=self.question, text_answer="Test answer"
        )
        expected = f"Answer to {self.question.title[:30]}"
        self.assertEqual(str(answer), expected)

    def test_answer_unique_constraint(self):
        AnswerFactory(
            response=self.response, question=self.question, text_answer="First answer"
        )
        with self.assertRaises():
            AnswerFactory(
                response=self.response,
                question=self.question,
                text_answer="Second answer",
            )
