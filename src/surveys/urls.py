from django.urls import path

from surveys.views.answer import AnswerListCreateView, AnswerRetrieveView
from surveys.views.survey import (
    SurveyListCreateView,
    SurveyReportView,
    SurveyRetrieveUpdateDeleteView,
    SurveySendView,
)

urlpatterns = [
    # surveys
    path("api/v1/surveys", SurveyListCreateView.as_view(), name="surveys"),
    path(
        "api/v1/surveys/<int:pk>",
        SurveyRetrieveUpdateDeleteView.as_view(),
        name="survey_details",
    ),
    # survey answers
    path(
        "api/v1/surveys/<int:pk>/answers",
        AnswerListCreateView.as_view(),
        name="submit_survey",
    ),
    path(
        "api/v1/surveys/<int:survey_id>/answers/<str:uuid>",
        AnswerRetrieveView.as_view(),
        name="submit_survey_detail",
    ),
    # survey send to other user
    path("api/v1/surveys/<int:pk>/send", SurveySendView.as_view(), name="send_survey"),
    # generate survey report
    path(
        "api/v1/surveys/<int:pk>/report",
        SurveyReportView.as_view(),
        name="survey_report",
    ),
]
