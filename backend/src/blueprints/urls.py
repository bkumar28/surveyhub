from blueprints.api.v1.urls import urlpatterns as v1_urls
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # Frontend URLs
    path(
        "blueprints/",
        TemplateView.as_view(template_name="blueprints/list.html"),
        name="list",
    ),
    path("api/v1/blueprints/", include(v1_urls)),
]
