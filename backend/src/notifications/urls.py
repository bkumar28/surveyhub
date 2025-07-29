from django.urls import path
from django.views.generic import TemplateView
from notifications.api.v1.urls import urlpatterns as v1_urls

urlpatterns = [
    # Frontend URLs
    path(
        "notifications/",
        TemplateView.as_view(template_name="notifications/list.html"),
        name="list",
    ),
] + v1_urls
