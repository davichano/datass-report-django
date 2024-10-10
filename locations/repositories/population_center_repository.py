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
