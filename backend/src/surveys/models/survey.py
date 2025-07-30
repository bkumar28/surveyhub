import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Use get_user_model for better custom user model support
User = get_user_model()


class SurveyStatus(models.TextChoices):
    """Enumerates the various statuses a survey can be in."""

    DRAFT = "D", "Draft"
    ACTIVE = "A", "Active"
    PAUSED = "P", "Paused"
    COMPLETED = "C", "Completed"
    EXPIRED = "E", "Expired"


class SurveyVisibility(models.TextChoices):
    """Defines the visibility level of a survey."""

    PUBLIC = "PU", "Public"
    PRIVATE = "PR", "Private"
    INVITE_ONLY = "IN", "Invite Only"


class Survey(models.Model):
    """Main model representing a survey definition."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="surveys_created"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="surveys_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=1, choices=SurveyStatus.choices, default=SurveyStatus.DRAFT
    )
    visibility = models.CharField(
        max_length=2, choices=SurveyVisibility.choices, default=SurveyVisibility.PUBLIC
    )

    # Survey options
    is_anonymous = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    max_responses = models.IntegerField(null=True, blank=True)
    requires_login = models.BooleanField(default=False)
    allow_multiple_responses = models.BooleanField(default=False)
    show_progress_bar = models.BooleanField(default=True)
    thank_you_message = models.TextField(default="Thank you for your response!")

    # Branding
    theme_color = models.CharField(max_length=7, default="#007bff")
    logo = models.ImageField(upload_to="survey_logos/", null=True, blank=True)
    custom_css = models.TextField(blank=True)

    # Analytics
    response_count = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    average_time = models.DurationField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["created_by", "status"]),
        ]

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        """
        Determines whether the survey is currently active
        and within the time window.
        """
        now = timezone.now()
        return (
            self.status == SurveyStatus.ACTIVE
            and self.start_date <= now
            and (self.end_date is None or self.end_date >= now)
        )

    @property
    def response_limit_reached(self):
        """Checks if the survey has reached the maximum allowed responses."""
        return (
            self.max_responses is not None and self.response_count >= self.max_responses
        )


class SurveyResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(
        "surveys.Survey", on_delete=models.CASCADE, related_name="responses"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    user_token = models.UUIDField(default=uuid.uuid4, editable=False)

    # Response metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)

    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.DurationField(null=True, blank=True)

    # Status
    is_complete = models.BooleanField(default=False)
    is_test = models.BooleanField(default=False)

    # Location
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ["survey", "user_token"]
        ordering = ["-started_at", "id"]
        indexes = [
            models.Index(fields=["survey", "is_complete"]),
            models.Index(fields=["completed_at"]),
        ]

    def __str__(self):
        return f"Response to {self.survey.title} by {self.user or 'Anonymous'}"
