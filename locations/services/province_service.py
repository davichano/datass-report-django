from locations.repositories.province_repository import ProvinceRepository
from locations.serializers import ProvinceSerializer
from locations.services.district_service import DistrictService
from surveys.repositories.dataset_i_repository import DatasetIRepository


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

    @staticmethod
    def get_water_access_by_province(province_id):
        return ProvinceRepository.get_water_access_by_province(province_id)

    @staticmethod
    def get_water_access_for_all_provinces():
        last_ds_i_record = DatasetIRepository.get_last_year_month()
        last_year = last_ds_i_record.year if last_ds_i_record else None
        last_month = last_ds_i_record.month if last_ds_i_record else None
        if last_year is None or last_month is None:
            return None
        data = {
            "water_access": ProvinceRepository.get_water_access_for_all_provinces(last_year, last_month),
            "ubs_access": ProvinceRepository.get_ubs_access_for_all_provinces(last_year, last_month),
        }
        return data

    @classmethod
    def get_provinces_with_districts(cls):
        return {
            "provinces": ProvinceService.get_all(),
            "districts": DistrictService.get_all(),
        }
