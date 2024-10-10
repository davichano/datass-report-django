# reports/urls.py

from django.urls import path

from reports.views import ReportView

urlpatterns = [
    path("api/<str:report_name>/", ReportView.as_view(), name="reports"),
]
