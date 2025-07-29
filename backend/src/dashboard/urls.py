from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Frontend URLs
    path(
        "dashboard/",
        TemplateView.as_view(template_name="dashboard.html"),
        name="dashboard",
    ),
]
