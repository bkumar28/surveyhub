import factory
from surveys.models.question import Question, QuestionOption


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    id = factory.Faker("uuid4")
    survey = factory.SubFactory("surveys.tests.factories.survey_factory.SurveyFactory")
    title = factory.Faker("sentence")
    description = factory.Faker("sentence")
    field_type = "T"
    is_required = False
    order = factory.Sequence(lambda n: n)
    condition_value = ""
    condition_operator = ""
    depends_on = None
    min_length = None
    max_length = None
    min_value = None
    max_value = None
    regex_pattern = ""
    scale_min = 1
    scale_max = 5
    scale_labels = factory.Dict({})
    options = factory.List([])
    allow_other = False
    matrix_rows = factory.List([])
    matrix_columns = factory.List([])
    placeholder_text = ""
    help_text = ""
    validation_regex = ""
    error_message = ""


class QuestionOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuestionOption

    id = factory.Faker("uuid4")
    question = factory.SubFactory(
        "surveys.tests.factories.question_factory.QuestionFactory"
    )
    text = factory.Faker("word")
    value = factory.Faker("word")
    order = factory.Sequence(lambda n: n)
    is_other = False
