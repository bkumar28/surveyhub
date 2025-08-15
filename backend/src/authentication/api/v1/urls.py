from authentication.api.v1.viewsets.access_token import CustomTokenObtainPairView
from django.urls import path

urlpatterns = [
    path(
        "api/v1/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
]
