# report/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reports.services.report_service import ReportService


class ReportView(APIView):
    def get(self, request, report_name, *args, **kwargs):
        try:
            if report_name == "home_resume":
                data = ReportService.get_home_resume()
            elif report_name == "province_resume":
                name = request.GET.get("name")
                data = ReportService.get_province_resume(name)
            else:
                return Response({"error": "Invalid report name"}, status=status.HTTP_400_BAD_REQUEST)

            if data is None:
                return Response({"error": "No data available"}, status=status.HTTP_204_NO_CONTENT)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
