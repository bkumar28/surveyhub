import uuid

from django.db import models


class NotificationType(models.TextChoices):
    """Defines supported notification delivery channels."""

    EMAIL = "email", "Email"
    SMS = "sms", "SMS"
    WEBHOOK = "webhook", "Webhook"
    SLACK = "slack", "Slack"


class NotificationTemplate(models.Model):
    """Stores reusable notification templates for various channels and purposes."""

    TEMPLATE_TYPES = [
        ("INVITE", "Survey Invitation"),
        ("REMINDER", "Survey Reminder"),
        ("THANK_YOU", "Thank You Message"),
        ("COMPLETION", "Survey Completion"),
    ]

    name = models.CharField(max_length=255)
    notification_type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        help_text="Type of notification channel (e.g., Email, SMS, etc.)",
    )
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        help_text="Purpose or context of the notification",
    )
    subject = models.CharField(
        max_length=255,
        blank=True,
        help_text="Subject line for email or similar message types",
    )
    body = models.TextField(help_text="Main content body of the notification")
    template = models.TextField(
        help_text="Optional raw or templated version of the message body"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification Template"
        verbose_name_plural = "Notification Templates"

    def __str__(self):
        return f"{self.name} ({self.notification_type} - {self.template_type})"


class SurveyInvitation(models.Model):
    survey = models.ForeignKey(
        "surveys.Survey", on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    reminder_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ["survey", "email"]

    def __str__(self):
        return f"Invitation to {self.survey.title} for {self.email}"
