from analytics.api.v1.viewsets import QuestionAnalyticsViewSet, SurveyAnalyticsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"api/v1/survey-analytics", SurveyAnalyticsViewSet, basename="survey-analytics"
)
router.register(
    r"api/v1/question-analytics",
    QuestionAnalyticsViewSet,
    basename="question-analytics",
)

urlpatterns = router.urls
