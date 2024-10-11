# location/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from locations.services.population_center_service import PopulationCenterService
from locations.services.province_service import ProvinceService


class ProvinceView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get("option") == "list-p-d":
                data = ProvinceService.get_provinces_with_districts()
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = ProvinceService.get_water_access_for_all_provinces()
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PopulationCenterView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get("option") == "by-district":
                district_id = request.GET.get("district")
                data = PopulationCenterService.get_all_by_district(district_id)
                return Response(data, status=status.HTTP_200_OK)
            data = PopulationCenterService.get_all()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
