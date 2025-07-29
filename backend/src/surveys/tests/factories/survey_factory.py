import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker
from surveys.models.survey import Survey, SurveyResponse, SurveyStatus, SurveyVisibility

fake = Faker()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Avoid saving the user after creation

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass")


class SurveyFactory(DjangoModelFactory):
    class Meta:
        model = Survey

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.LazyAttribute(lambda obj: obj.created_by)
    start_date = factory.LazyFunction(timezone.now)
    end_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=7))
    status = SurveyStatus.ACTIVE
    visibility = SurveyVisibility.PUBLIC
    is_anonymous = True
    is_public = False
    max_responses = 100
    requires_login = False
    allow_multiple_responses = False
    show_progress_bar = True
    thank_you_message = factory.Faker("sentence")
    theme_color = "#00aaff"
    custom_css = ""
    response_count = 0
    completion_rate = 0.0
    average_time = None


class SurveyResponseFactory(DjangoModelFactory):
    class Meta:
        model = SurveyResponse

    survey = factory.SubFactory(SurveyFactory)
    user = factory.SubFactory(UserFactory)
    session_key = factory.Faker("uuid4")
    ip_address = factory.Faker("ipv4")
    user_agent = factory.Faker("user_agent")
    referrer = factory.Faker("url")
    started_at = factory.LazyFunction(timezone.now)
    completed_at = factory.LazyAttribute(
        lambda o: o.started_at + timezone.timedelta(minutes=5)
    )
    time_taken = factory.LazyAttribute(lambda o: o.completed_at - o.started_at)
    is_complete = False
    is_test = False
    country = factory.Faker("country")
    city = factory.Faker("city")
