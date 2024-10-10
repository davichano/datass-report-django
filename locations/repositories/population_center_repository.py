from locations.models import PopulationCenter


class PopulationCenterRepository:

    @staticmethod
    def get_all():
        return PopulationCenter.objects.all()

    @staticmethod
    def get_by_id(id):
        try:
            return PopulationCenter.objects.get(id=id)
        except PopulationCenter.DoesNotExist:
            return PopulationCenter()

    @staticmethod
    def get_by_code(code):
        try:
            return PopulationCenter.objects.get(code=code)
        except PopulationCenter.DoesNotExist:
            return PopulationCenter()

    @staticmethod
    def save(population_center):
        population_center.save()
        return population_center

    @staticmethod
    def get_all_by_district(district_id):
        return PopulationCenter.objects.filter(district=district_id)

    @staticmethod
    def get_total_with_99():
        return PopulationCenter.objects.filter(code__regex=r"^.{6}99").count()

    @staticmethod
    def get_total_with_99_by_province(province_id):
        return PopulationCenter.objects.filter(
            district__province_id=province_id, code__regex=r"^.{6}99"
        ).count()

    @staticmethod
    def get_total():
        return PopulationCenter.objects.count()

    @staticmethod
    def get_total_by_province(province_id):
        return PopulationCenter.objects.filter(district__province_id=province_id).count()

    @staticmethod
    def get_total_with_water(year, month):
        return PopulationCenter.objects.filter(
            dataset_i_records__year=year,
            dataset_i_records__month=month,
            dataset_i_records__has_water_system=True,
        ).count()

    @staticmethod
    def get_total_with_water_by_province(year, month, province_id):
        return PopulationCenter.objects.filter(
            district__province_id=province_id,
            dataset_i_records__year=year,
            dataset_i_records__month=month,
            dataset_i_records__has_water_system=True,
        ).count()

    @staticmethod
    def get_total_with_sanitation(year, month):
        return PopulationCenter.objects.filter(
            dataset_i_records__year=year,
            dataset_i_records__month=month,
            dataset_i_records__has_sanitation_system=True,
        ).count()

    @staticmethod
    def get_total_with_sanitation_by_province(year, month, province_id):
        return PopulationCenter.objects.filter(
            district__province_id=province_id,
            dataset_i_records__year=year,
            dataset_i_records__month=month,
            dataset_i_records__has_sanitation_system=True,
        ).count()
