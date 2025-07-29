import factory
from django.utils import timezone
from notifications.models import Notification, NotificationTemplate, NotificationType
from surveys.tests.factories.survey_factory import SurveyFactory


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    survey = factory.SubFactory(SurveyFactory)
    email = factory.Faker("email")
    token = factory.Faker("uuid4")
    sent_at = factory.LazyFunction(lambda: timezone.now())
    opened_at = None
    responded_at = None
    reminder_count = 0


class NotificationTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NotificationTemplate

    name = factory.Faker("word")
    notification_type = NotificationType.EMAIL
    template_type = "INVITE"
    subject = factory.Faker("sentence")
    body = factory.Faker("text")
    template = factory.Faker("text")
    is_active = True
