# reports/urls.py

from django.urls import path

from reports.views import ReportView, SystemView

urlpatterns = [
    path("api/general/<str:report_name>/", ReportView.as_view(), name="reports"),
    path("api/systems/<str:report_name>/", SystemView.as_view(), name="reports_systems"),
]
