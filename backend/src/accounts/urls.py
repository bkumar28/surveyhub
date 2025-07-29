from accounts.api.v1.urls import urlpatterns as api_v1_urls
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "profile/",
        TemplateView.as_view(template_name="account/profile.html"),
        name="profile",
    ),
] + api_v1_urls
