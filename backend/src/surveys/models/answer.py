import json
import uuid

from django.db import models


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    response = models.ForeignKey(
        "surveys.SurveyResponse", on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey("surveys.Question", on_delete=models.CASCADE)

    # Different answer types
    text_answer = models.TextField(blank=True)
    number_answer = models.FloatField(null=True, blank=True)
    date_answer = models.DateField(null=True, blank=True)
    datetime_answer = models.DateTimeField(null=True, blank=True)
    file_answer = models.FileField(upload_to="survey_files/", null=True, blank=True)
    json_answer = models.JSONField(default=dict, blank=True)  # For complex answers

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["response", "question"]
        indexes = [
            models.Index(fields=["question", "created_at"]),
        ]

    def __str__(self):
        return f"Answer to {self.question.title[:30]}"

    @property
    def display_value(self):
        """Return the appropriate answer value based on question type"""
        if self.text_answer:
            return self.text_answer
        elif self.number_answer is not None:
            return str(self.number_answer)
        elif self.date_answer:
            return self.date_answer.strftime("%Y-%m-%d")
        elif self.datetime_answer:
            return self.datetime_answer.strftime("%Y-%m-%d %H:%M")
        elif self.json_answer:
            return json.dumps(self.json_answer)
        return ""
