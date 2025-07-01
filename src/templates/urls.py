from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    QuestionTemplateViewSet,
    SurveyTemplateViewSet,
    TemplateCategoryViewSet,
)

router = DefaultRouter()
router.register(r"categories", TemplateCategoryViewSet)
router.register(r"surveys", SurveyTemplateViewSet)
router.register(r"questions", QuestionTemplateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
