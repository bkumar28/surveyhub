from django.urls import path
from django.views.generic import TemplateView
from surveys.api.v1.urls import urlpatterns as v1_urls

urlpatterns = [
    # Frontend URLs for surveys
    path(
        "surveys/",
        TemplateView.as_view(template_name="surveys/list.html"),
        name="surveys_list",
    ),
    # Frontend URLs for questions
    path(
        "survey-questions/",
        TemplateView.as_view(template_name="questions/list.html"),
        name="questions_list",
    ),
    path(
        "survey-questions/form/",
        TemplateView.as_view(template_name="questions/form.html"),
        name="questions_create",
    ),
    path(
        "survey-questions/form/<int:id>/",
        TemplateView.as_view(template_name="questions/form.html"),
        name="questions_edit",
    ),
    path(
        "survey-questions/detail/<int:id>/",
        TemplateView.as_view(template_name="questions/detail.html"),
        name="questions_detail",
    ),
    # Frontend URLs for responses
    path(
        "survey-responses/",
        TemplateView.as_view(template_name="responses/list.html"),
        name="responses_list",
    ),
    path(
        "survey-responses/form/",
        TemplateView.as_view(template_name="responses/form.html"),
        name="responses_create",
    ),
    path(
        "responses/form/<int:id>/",
        TemplateView.as_view(template_name="responses/form.html"),
        name="responses_edit",
    ),
    path(
        "survey-responses/detail/<int:id>/",
        TemplateView.as_view(template_name="responses/detail.html"),
        name="responses_detail",
    ),
] + v1_urls
