# locations/urls.py
from django.urls import path

from locations.views import ProvinceView

urlpatterns = [
    path("provinces/", ProvinceView.as_view(), name="province"),
]
