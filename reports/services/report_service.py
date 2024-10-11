# reports/services/report_service.py
from locations.repositories.district_repository import DistrictRepository
from locations.repositories.population_center_repository import PopulationCenterRepository
from locations.repositories.province_repository import ProvinceRepository
from locations.serializers import ProvinceSerializer
from surveys.repositories.dataset_i_repository import DatasetIRepository


class ReportService:
    @staticmethod
    def get_home_resume():
        last_ds_i_record = DatasetIRepository.get_last_year_month()
        last_year = last_ds_i_record.year if last_ds_i_record else None
        last_month = last_ds_i_record.month if last_ds_i_record else None
        if last_year is None or last_month is None:
            return None
        people_resume = DatasetIRepository.get_totals_by_year_month(last_year, last_month)
        data = {
            "total_pc": PopulationCenterRepository.get_total(),
            "total_pc_with_water": PopulationCenterRepository.get_total_with_water(last_year, last_month),
            "total_pc_with_sanitation": PopulationCenterRepository.get_total_with_sanitation(
                last_year, last_month
            ),
            "total_pc_with_99": PopulationCenterRepository.get_total_with_99(),
            **people_resume,
        }
        return data

    @classmethod
    def get_province_resume(cls, name):
        province = ProvinceRepository.get_by_name(name)
        if province.id is None:
            return None
        last_ds_i_record = DatasetIRepository.get_last_year_month()
        last_year = last_ds_i_record.year if last_ds_i_record else None
        last_month = last_ds_i_record.month if last_ds_i_record else None
        if last_year is None or last_month is None:
            return None
        people_resume = DatasetIRepository.get_totals_by_year_month_province(
            last_year, last_month, province.id
        )
        province_data = ProvinceSerializer(province).data
        province_data.points = province.get_centroid()
        province_data_with_centroid = {**province_data, "points": province.get_centroid()}

        data = {
            "province": province_data_with_centroid,
            "total_pc": PopulationCenterRepository.get_total_by_province(province.id),
            "total_pc_with_water": PopulationCenterRepository.get_total_with_water_by_province(
                last_year, last_month, province.id
            ),
            "total_pc_with_sanitation": PopulationCenterRepository.get_total_with_sanitation_by_province(
                last_year, last_month, province.id
            ),
            "total_pc_with_99": PopulationCenterRepository.get_total_with_99_by_province(province.id),
            "water_access": DistrictRepository.get_water_access_by_province(
                province.id, last_year, last_month
            ),
            "ubs_access": DistrictRepository.get_ubs_access_by_province(province.id, last_year, last_month),
            "houses_water": DistrictRepository.get_water_houses_by_province(
                province.id, last_year, last_month
            ),
            "houses_ubs": DistrictRepository.get_ubs_houses_by_province(province.id, last_year, last_month),
            **people_resume,
        }
        return data
