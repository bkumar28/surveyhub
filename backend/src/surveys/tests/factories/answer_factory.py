import factory
from surveys.models.answer import Answer


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    id = factory.Faker("uuid4")
    response = factory.SubFactory(
        "surveys.tests.factories.survey_factory.SurveyResponseFactory"
    )
    question = factory.SubFactory(
        "surveys.tests.factories.question_factory.QuestionFactory"
    )

    # Default empty string for text_answer (not NULL)
    text_answer = ""
    number_answer = None
    date_answer = None
    datetime_answer = None
    file_answer = None
    json_answer = factory.Dict({})
