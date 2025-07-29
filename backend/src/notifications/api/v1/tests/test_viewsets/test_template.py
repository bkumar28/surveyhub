from django.urls import reverse
from notifications.models import NotificationTemplate
from notifications.tests.factories import NotificationTemplateFactory
from rest_framework.test import APITestCase


class NotificationTemplateViewSetTest(APITestCase):
    def setUp(self):
        self.template = NotificationTemplateFactory()
        self.list_url = reverse("notifications:notificationtemplate-list")
        self.detail_url = reverse(
            "notifications:notificationtemplate-detail", args=[self.template.id]
        )

    def test_list_templates(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        # Adjust for custom response structure
        results = response.data.get("data", {}).get("results", [])
        self.assertTrue(
            any(
                isinstance(t, dict) and t.get("id") == str(self.template.id)
                for t in results
            )
        )

    def test_retrieve_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.template.id))

    def test_create_template(self):
        data = {
            "name": "Test Template",
            "notification_type": "email",
            "template_type": "INVITE",
            "subject": "Test Subject",
            "body": "Test Body",
            "template": "Test Template",
            "is_active": True,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            NotificationTemplate.objects.filter(name="Test Template").exists()
        )

    def test_update_template(self):
        data = {"name": "Updated Name"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, 200)
        self.template.refresh_from_db()
        self.assertEqual(self.template.name, "Updated Name")

    def test_delete_template(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            NotificationTemplate.objects.filter(id=self.template.id).exists()
        )
