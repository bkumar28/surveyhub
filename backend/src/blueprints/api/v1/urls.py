from blueprints.api.v1.viewsets.blueprint import (
    QuestionBlueprintViewSet,
    SurveyBlueprintViewSet,
)
from blueprints.api.v1.viewsets.category import (
    BlueprintCategoryViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", BlueprintCategoryViewSet, basename="blueprintcategory")
router.register(r"surveys", SurveyBlueprintViewSet, basename="surveyblueprint")
router.register(r"questions", QuestionBlueprintViewSet, basename="questionblueprint")

urlpatterns = router.urls
