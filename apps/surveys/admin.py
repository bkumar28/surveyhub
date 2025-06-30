from django.contrib import admin

from survey.models.answer import Answer
from survey.models.question import Question
from survey.models.survey import Survey, SurveyInvitation

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(SurveyInvitation)