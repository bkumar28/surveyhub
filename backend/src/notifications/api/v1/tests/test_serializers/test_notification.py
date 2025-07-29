from django.test import TestCase
from notifications.api.v1.serializers.notification import SurveyInvitationSerializer
from notifications.tests.factories import NotificationFactory


class SurveyInvitationSerializerTest(TestCase):
    def setUp(self):
        self.notification = NotificationFactory()
        self.serializer = SurveyInvitationSerializer(instance=self.notification)

    def test_serialized_data(self):
        data = self.serializer.data
        self.assertEqual(data["email"], self.notification.email)
        self.assertEqual(data["token"], str(self.notification.token))
