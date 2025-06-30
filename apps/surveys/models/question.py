from django.db import models
from django.utils.translation import gettext_lazy as _  
from django.core.validators import MinValueValidator, MaxValueValidator


class QuestionType(models.TextChoices):
    TEXT = 'T', _('Text')
    NUMBER = 'N', _('Number')
    EMAIL = 'E', _('Email')
    MULTIPLE_CHOICE = 'MC', _('Multiple Choice')
    CHECKBOX = 'CB', _('Checkbox')
    RADIO = 'RD', _('Radio')
    RATING = 'RT', _('Rating')
    DATE = 'DT', _('Date')
    DATETIME = 'DTM', _('DateTime')
    FILE = 'FL', _('File')
    MATRIX = 'MX', _('Matrix')
    SLIDER = 'SL', _('Slider')
    YES_NO = 'YN', _('Yes/No')


class Question(models.Model):
    survey = models.ForeignKey(
        "surveys.Survey",
        on_delete=models.CASCADE,
        related_name='questions'
    )
    title = models.TextField()
    description = models.TextField(blank=True)
    field_type = models.CharField(max_length=3, choices=QuestionType.choices)
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    # Advanced options
    placeholder_text = models.CharField(max_length=255, blank=True)
    help_text = models.TextField(blank=True)
    validation_regex = models.CharField(max_length=255, blank=True)
    error_message = models.CharField(max_length=255, blank=True)

    # Rating-specific fields
    rating_min = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    rating_max = models.IntegerField(default=5, validators=[MaxValueValidator(10)])
    rating_labels = models.JSONField(default=dict, blank=True)

    # Number-specific fields
    number_min = models.FloatField(null=True, blank=True)
    number_max = models.FloatField(null=True, blank=True)

    # File upload settings
    allowed_file_types = models.CharField(max_length=255, blank=True)
    max_file_size = models.IntegerField(default=5)  # in MB

    # Conditional logic
    conditional_logic = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        indexes = [
            models.Index(fields=['survey', 'order']),
        ]

    def __str__(self):
        return f"{self.survey.title} - {self.title[:50]}"


class QuestionOption(models.Model):
    question = models.ForeignKey(
        "surveys.Question",
        on_delete=models.CASCADE,
        related_name='options'
    )
    text = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_other = models.BooleanField(default=False)  # For "Other" option

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.question.title[:30]} - {self.text}"
