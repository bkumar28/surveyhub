import uuid

from django.db import models


class SurveyAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.OneToOneField(
        "surveys.Survey", on_delete=models.CASCADE, related_name="analytics"
    )

    # Response metrics
    total_views = models.IntegerField(default=0)
    total_starts = models.IntegerField(default=0)
    total_completions = models.IntegerField(default=0)

    # Time metrics
    average_completion_time = models.DurationField(null=True, blank=True)
    median_completion_time = models.DurationField(null=True, blank=True)

    # Engagement metrics
    bounce_rate = models.FloatField(default=0.0)  # Started but didn't complete
    completion_rate = models.FloatField(default=0.0)

    # Device analytics
    mobile_responses = models.IntegerField(default=0)
    desktop_responses = models.IntegerField(default=0)
    tablet_responses = models.IntegerField(default=0)

    # Geographic data
    top_countries = models.JSONField(default=dict)
    top_cities = models.JSONField(default=dict)

    # Traffic sources
    traffic_sources = models.JSONField(default=dict)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.survey.title}"

    class Meta:
        ordering = ["-updated_at", "-id"]


class QuestionAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.OneToOneField(
        "surveys.Question", on_delete=models.CASCADE, related_name="analytics"
    )

    # Response metrics
    total_answers = models.IntegerField(default=0)
    skip_count = models.IntegerField(default=0)

    # Text analysis (for text questions)
    word_cloud_data = models.JSONField(default=dict)
    sentiment_score = models.FloatField(null=True, blank=True)

    # Choice analysis (for multiple choice)
    choice_distribution = models.JSONField(default=dict)

    # Numeric analysis
    average_value = models.FloatField(null=True, blank=True)
    median_value = models.FloatField(null=True, blank=True)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.question.title[:50]}"

    class Meta:
        ordering = ["-updated_at", "-id"]
