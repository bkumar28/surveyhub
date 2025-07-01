from django.contrib import admin
from surveys.models.answer import Answer
from surveys.models.question import Question
from surveys.models.survey import Survey

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
