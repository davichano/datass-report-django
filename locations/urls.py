# locations/urls.py
from django.urls import path

from locations.views import ProvinceView, PopulationCenterView

urlpatterns = [
    path("provinces/", ProvinceView.as_view(), name="province"),
    path("population-centers/", PopulationCenterView.as_view(), name="population-center"),
]
