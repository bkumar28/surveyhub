from django.test import TestCase
from surveys.models.question import FieldType, Question
from surveys.tests.factories.question_factory import (
    QuestionFactory,
    QuestionOptionFactory,
)
from surveys.tests.factories.survey_factory import SurveyFactory, UserFactory


class QuestionModelTest(TestCase):
    """Test cases for Question model"""

    def setUp(self):
        """Set up test data"""
        self.user = UserFactory()
        self.survey = SurveyFactory(created_by=self.user)
        self.question = QuestionFactory(survey=self.survey)
        self.option = QuestionOptionFactory(question=self.question)

    def test_question_creation(self):
        """Test question creation with valid data"""
        question = QuestionFactory(
            survey=self.survey,
            title="Test Question",
            description="A test question",
            field_type=FieldType.TEXT,
            is_required=True,
            order=1,
            min_length=5,
            max_length=100,
            placeholder_text="Enter your answer",
            help_text="Please provide a detailed answer",
        )

        self.assertEqual(question.survey, self.survey)
        self.assertEqual(question.title, "Test Question")
        self.assertEqual(question.description, "A test question")
        self.assertEqual(question.field_type, FieldType.TEXT)
        self.assertTrue(question.is_required)
        self.assertEqual(question.order, 1)
        self.assertEqual(question.min_length, 5)
        self.assertEqual(question.max_length, 100)
        self.assertEqual(question.placeholder_text, "Enter your answer")
        self.assertEqual(question.help_text, "Please provide a detailed answer")

    def test_question_str_method(self):
        """Test question string representation"""
        # Create survey with known title
        survey = SurveyFactory(created_by=self.user, title="Test Survey")
        # Create question with known title
        question = QuestionFactory(survey=survey, title="Test Question")
        # The expected string is the actual string representation
        expected = "Test Survey - Test Question"
        self.assertEqual(str(question), expected)

    def test_question_rating_fields(self):
        """Test rating question specific fields"""
        question = QuestionFactory(
            survey=self.survey,
            field_type=FieldType.RATING,
            scale_min=1,
            scale_max=5,
            scale_labels={"1": "Poor", "5": "Excellent"},
        )

        self.assertEqual(question.scale_min, 1)
        self.assertEqual(question.scale_max, 5)
        self.assertEqual(question.scale_labels, {"1": "Poor", "5": "Excellent"})

    def test_question_multiple_choice_fields(self):
        """Test multiple choice question specific fields"""
        question = QuestionFactory(
            survey=self.survey,
            field_type=FieldType.MULTIPLE_CHOICE,
            options=["Option 1", "Option 2", "Option 3"],
            allow_other=True,
        )

        self.assertEqual(question.options, ["Option 1", "Option 2", "Option 3"])
        self.assertTrue(question.allow_other)

    def test_question_matrix_fields(self):
        """Test matrix question specific fields"""
        question = QuestionFactory(
            survey=self.survey,
            field_type=FieldType.MATRIX,
            matrix_rows=["Row 1", "Row 2"],
            matrix_columns=["Column 1", "Column 2"],
        )

        self.assertEqual(question.matrix_rows, ["Row 1", "Row 2"])
        self.assertEqual(question.matrix_columns, ["Column 1", "Column 2"])

    def test_question_conditional_logic(self):
        """Test question conditional logic"""
        parent_question = QuestionFactory(survey=self.survey, title="Parent Question")

        conditional_question = QuestionFactory(
            survey=self.survey,
            title="Conditional Question",
            order=2,
            depends_on=parent_question,
            condition_value="Yes",
            condition_operator="equals",
        )

        self.assertEqual(conditional_question.depends_on, parent_question)
        self.assertEqual(conditional_question.condition_value, "Yes")
        self.assertEqual(conditional_question.condition_operator, "equals")

    def test_question_ordering(self):
        """Test question ordering"""
        # Make sure we create questions with explicit order values
        # and clear existing questions
        Question.objects.all().delete()

        # Create questions with known orders and IDs to ensure deterministic results
        question1 = QuestionFactory(survey=self.survey, order=1, title="Question 1")
        question2 = QuestionFactory(survey=self.survey, order=2, title="Question 2")

        # Get all questions ordered by order field explicitly
        questions = list(Question.objects.all().order_by("order"))

        # Compare by ID which is more reliable than comparing whole objects
        self.assertEqual(str(questions[0].id), question1.id)  # Lower order first
        self.assertEqual(str(questions[1].id), question2.id)  # Higher order second


class QuestionOptionModelTest(TestCase):
    """Test cases for QuestionOption model"""

    def setUp(self):
        """Set up test data"""
        self.user = UserFactory()
        self.survey = SurveyFactory(created_by=self.user)
        self.question = QuestionFactory(
            survey=self.survey, field_type=FieldType.SINGLE_CHOICE
        )

    def test_question_option_creation(self):
        """Test question option creation"""
        option = QuestionOptionFactory(
            question=self.question,
            text="Option 1",
            value="option1",
            order=1,
            is_other=False,
        )

        self.assertEqual(option.question, self.question)
        self.assertEqual(option.text, "Option 1")
        self.assertEqual(option.value, "option1")
        self.assertEqual(option.order, 1)
        self.assertFalse(option.is_other)

    def test_question_option_str_method(self):
        """Test question option string representation"""
        option = QuestionOptionFactory(
            question=self.question, text="Option 1", value="option1", order=1
        )

        expected = f"{self.question.title[:30]} - Option 1"
        self.assertEqual(str(option), expected)

    def test_question_option_other(self):
        """Test 'other' option"""
        option = QuestionOptionFactory(
            question=self.question,
            text="Other",
            value="other",
            order=999,
            is_other=True,
        )

        self.assertTrue(option.is_other)
