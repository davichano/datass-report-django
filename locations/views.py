# location/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from locations.services.province_service import ProvinceService


class ProvinceView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = ProvinceService.get_water_access_for_all_provinces()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
