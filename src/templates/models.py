from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TemplateCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Template Categories'

    def __str__(self):
        return self.name


class SurveyTemplate(models.Model):
    """Model to represent a reusable survey template."""

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        TemplateCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='survey_templates'
    )
    tags = models.JSONField(default=list, help_text="List of tags for filtering/search.")
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_survey_templates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)

    template_data = models.JSONField(help_text="JSON representation of the survey structure.")
    preview_image = models.ImageField(
        upload_to='template_previews/',
        null=True,
        blank=True,
        help_text="Optional preview image for the template."
    )

    class Meta:
        ordering = ['-usage_count', '-created_at']

    def __str__(self):
        return self.name

    def use_template(self):
        """Increments usage count each time the template is used."""
        self.usage_count += 1
        self.save(update_fields=["usage_count"])


class QuestionTemplate(models.Model):
    """Pre-built question templates for reuse across surveys."""

    title = models.CharField(max_length=200)
    field_type = models.CharField(max_length=3, help_text="Field type code, e.g., 'TXT', 'MCQ'")
    category = models.CharField(max_length=50)
    template_data = models.JSONField(default=dict, help_text="JSON structure of the question.")
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-usage_count', 'title']

    def __str__(self):
        return self.title
