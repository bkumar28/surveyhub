import uuid
from django.db import models


class NotificationType(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    WEBHOOK = 'webhook', 'Webhook'
    SLACK = 'slack', 'Slack'


class NotificationTemplate(models.Model):
    name = models.CharField(max_length=255)
    notification_type = models.CharField(
        max_length=10,
        choices=NotificationType.choices
    )
    subject = models.CharField(max_length=255, blank=True)
    template = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.notification_type})"


class SurveyInvitation(models.Model):
    survey = models.ForeignKey(
        "surveys.Survey",
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    reminder_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['survey', 'email']

    def __str__(self):
        return f"Invitation to {self.survey.title} for {self.email}"
