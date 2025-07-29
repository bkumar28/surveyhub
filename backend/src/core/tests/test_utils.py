import unittest
from unittest.mock import MagicMock, patch

from core import utils
from django.http import HttpResponse


class TestUtils(unittest.TestCase):
    def test_export_survey_responses_csv(self):
        survey = MagicMock()
        survey.title = "TestSurvey"
        survey.questions.all.return_value = [
            MagicMock(title="Q1"),
            MagicMock(title="Q2"),
        ]
        response1 = MagicMock()
        response1.id = 1
        response1.submitted_at = "2025-07-19"
        response1.user.username = "user1"
        response1.is_complete = True
        answer1 = MagicMock()
        answer1.text_answer = "A1"
        answer1.number_answer = 42
        answer1.boolean_answer = True
        answer1.choice_answers = ["C1", "C2"]
        response1.answers.get.side_effect = lambda question: answer1
        survey.responses.all.return_value = [response1]
        with patch("django.http.HttpResponse", wraps=HttpResponse):
            resp = utils.export_survey_responses_csv(survey)
            self.assertIsInstance(resp, HttpResponse)
            self.assertIn("TestSurvey_responses.csv", resp["Content-Disposition"])
