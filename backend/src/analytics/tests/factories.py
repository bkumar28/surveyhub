import factory
from analytics.models import QuestionAnalytics, SurveyAnalytics
from surveys.tests.factories.question_factory import QuestionFactory
from surveys.tests.factories.survey_factory import SurveyFactory


class SurveyAnalyticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SurveyAnalytics

    survey = factory.SubFactory(SurveyFactory)
    total_views = 10
    total_starts = 5
    total_completions = 3


class QuestionAnalyticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuestionAnalytics

    question = factory.SubFactory(QuestionFactory)
    total_answers = 7
    skip_count = 2
