from locations.repositories.district_repository import DistrictRepository
from locations.serializers import DistrictSerializer


class DistrictService:

    @staticmethod
    def get_all():
        districts = DistrictRepository.get_all()
        return DistrictSerializer(districts, many=True).data

    @staticmethod
    def get_by_province(province_id):
        districts = DistrictRepository.get_by_province(province_id)
        return DistrictSerializer(districts, many=True).data

    @staticmethod
    def get_by_id(district_id):
        district = DistrictRepository.get_by_id(district_id)
        return DistrictSerializer(district).data

    @staticmethod
    def get_by_name(name):
        district = DistrictRepository.get_by_name(name)
        return DistrictSerializer(district).data

    @staticmethod
    def save(district):
        district = DistrictRepository.save(district)
        return DistrictSerializer(district).data
