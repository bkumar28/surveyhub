import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class FieldType(models.TextChoices):
    """Defines the supported question field types."""

    TEXT = "T", "Text"
    TEXTAREA = "TA", "Textarea"
    NUMBER = "N", "Number"
    EMAIL = "E", "Email"
    SINGLE_CHOICE = "SC", "Single Choice"
    MULTIPLE_CHOICE = "MC", "Multiple Choice"
    RATING = "R", "Rating"
    SCALE = "S", "Scale"
    DATE = "D", "Date"
    DATETIME = "DT", "DateTime"
    BOOLEAN = "B", "Boolean"
    FILE_UPLOAD = "F", "File Upload"
    URL = "URL", "URL"
    PHONE = "PH", "Phone"
    MATRIX = "MAT", "Matrix"


class Question(models.Model):
    """Model representing a single question in a survey."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(
        "Survey", on_delete=models.CASCADE, related_name="questions"
    )
    title = models.TextField()
    description = models.TextField(blank=True)

    field_type = models.CharField(max_length=5, choices=FieldType.choices)
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    # Conditional Logic
    depends_on = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Optional parent question this one depends on",
    )
    condition_value = models.TextField(blank=True)
    condition_operator = models.CharField(
        max_length=20,
        blank=True,
        help_text="Operator for conditional logic (e.g., equals, contains)",
    )

    # Validation Rules
    min_length = models.IntegerField(null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    min_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    regex_pattern = models.CharField(
        max_length=200, blank=True, help_text="Optional regex to validate input"
    )

    # Scale or Rating
    scale_min = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    scale_max = models.IntegerField(default=5, validators=[MaxValueValidator(5)])
    scale_labels = models.JSONField(
        default=dict, blank=True, help_text="E.g., {1: 'Poor', 5: 'Excellent'}"
    )

    # Multiple Choice
    options = models.JSONField(
        default=list, blank=True, help_text="List of choices for MCQ/SCQ fields"
    )
    allow_other = models.BooleanField(default=False)

    # Matrix
    matrix_rows = models.JSONField(
        default=list, blank=True, help_text="List of row labels for matrix"
    )
    matrix_columns = models.JSONField(
        default=list, blank=True, help_text="List of column labels for matrix"
    )

    # Advanced options
    placeholder_text = models.CharField(max_length=255, blank=True)
    help_text = models.TextField(blank=True)
    validation_regex = models.CharField(max_length=255, blank=True)
    error_message = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = ["survey", "order"]

    def __str__(self):
        return f"{self.survey.title} - {self.title[:50]}"


class QuestionOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_options"
    )
    text = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_other = models.BooleanField(default=False)  # For "Other" option

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.question.title[:30]} - {self.text}"
