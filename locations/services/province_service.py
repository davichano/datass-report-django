from locations.repositories.province_repository import ProvinceRepository
from locations.serializers import ProvinceSerializer


class ProvinceService:
    @staticmethod
    def get_all():
        provinces = ProvinceRepository.get_all()
        return ProvinceSerializer(provinces, many=True).data

    @staticmethod
    def get_by_id(province_id):
        province = ProvinceRepository.get_by_id(province_id)
        return ProvinceSerializer(province).data

    @staticmethod
    def get_by_name(province_name):
        province = ProvinceRepository.get_by_name(province_name)
        return ProvinceSerializer(province).data

    @staticmethod
    def save(province):
        province = ProvinceRepository.save(province)
        return ProvinceSerializer(province).data
