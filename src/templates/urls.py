from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TemplateCategoryViewSet,
    SurveyTemplateViewSet,
    QuestionTemplateViewSet,
)

router = DefaultRouter()
router.register(r'categories', TemplateCategoryViewSet)
router.register(r'surveys', SurveyTemplateViewSet)
router.register(r'questions', QuestionTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
