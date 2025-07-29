from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from surveys.api.v1.viewsets.question import QuestionViewSet
from surveys.api.v1.viewsets.response import SurveyResponseViewSet
from surveys.api.v1.viewsets.survey import SurveyViewSet

# Main router for surveys
router = DefaultRouter()
router.register(r"api/v1/surveys", SurveyViewSet, basename="survey")
router.register(r"api/v1/questions", QuestionViewSet, basename="question")
router.register(
    r"api/v1/survey-responses", SurveyResponseViewSet, basename="survey-response"
)

# Nested routers for questions and responses under surveys
surveys_router = NestedDefaultRouter(router, r"api/v1/surveys", lookup="survey")
surveys_router.register(r"questions", QuestionViewSet, basename="question")
surveys_router.register(r"responses", SurveyResponseViewSet, basename="response")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(surveys_router.urls)),
]
