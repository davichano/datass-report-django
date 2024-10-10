from django.urls import path
from .views import CSVUploadView

urlpatterns = [
    path("api/upload/", CSVUploadView.as_view(), name="upload-csv"),
]
