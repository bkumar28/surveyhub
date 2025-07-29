from django.test import TestCase

from .factories import NotificationFactory, NotificationTemplateFactory


class NotificationModelTest(TestCase):
    def setUp(self):
        self.notification = NotificationFactory()

    def test_notification_creation(self):
        self.assertEqual(self.notification.email, self.notification.email)
        self.assertEqual(self.notification.reminder_count, 0)


class NotificationTemplateModelTest(TestCase):
    def setUp(self):
        self.template = NotificationTemplateFactory()

    def test_template_creation(self):
        self.assertEqual(self.template.name, self.template.name)
        self.assertTrue(self.template.is_active)
