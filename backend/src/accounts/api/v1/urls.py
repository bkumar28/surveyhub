from rest_framework.routers import DefaultRouter

from .viewsets import ProfileViewSet

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = router.urls
