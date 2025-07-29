from analytics.api.v1.urls import urlpatterns as v1_urls
from django.urls import path
from django.views.generic import TemplateView

app_name = "analytics"

urlpatterns = [
    path(
        "analytics/",
        TemplateView.as_view(template_name="analytics/survey.html"),
        name="dashboard",
    ),
    path(
        "question/",
        TemplateView.as_view(template_name="analytics/question.html"),
        name="question",
    ),
    path(
        "export/",
        TemplateView.as_view(template_name="analytics/survey.html"),
        name="export",
    ),  # Placeholder, you can implement this later
] + v1_urls
