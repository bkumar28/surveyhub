from django.test import TestCase
from notifications.api.v1.serializers.template import NotificationTemplateSerializer
from notifications.tests.factories import NotificationTemplateFactory


class NotificationTemplateSerializerTest(TestCase):
    def setUp(self):
        self.template = NotificationTemplateFactory()
        self.serializer = NotificationTemplateSerializer(instance=self.template)

    def test_serialized_data(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.template.name)
        self.assertEqual(data["notification_type"], self.template.notification_type)
