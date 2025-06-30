from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SurveyTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    tags = models.JSONField(default=list)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_count = models.IntegerField(default=0)

    # Template data
    template_data = models.JSONField()  # Survey structure
    preview_image = models.ImageField(upload_to='template_previews/', null=True, blank=True)

    class Meta:
        ordering = ['-usage_count', '-created_at']

    def __str__(self):
        return self.name


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
