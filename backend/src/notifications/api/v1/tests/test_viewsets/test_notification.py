from django.test import TestCase
from django.urls import reverse
from notifications.tests.factories import NotificationFactory
from rest_framework import status
from rest_framework.test import APIClient


class NotificationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.notification = NotificationFactory()
        self.list_url = reverse("notifications:notification-list")
        self.detail_url = reverse(
            "notifications:notification-detail", args=[self.notification.id]
        )

    def test_list_notifications(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_notification(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.notification.email)

    def test_update_notification(self):
        response = self.client.patch(
            self.detail_url, {"reminder_count": 1}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertEqual(self.notification.reminder_count, 1)
