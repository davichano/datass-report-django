from locations.repositories.population_center_repository import PopulationCenterRepository
from locations.serializers import PopulationCenterSerializer


class PopulationCenterService:
    @staticmethod
    def get_all():
        population_centers = PopulationCenterRepository.get_all()
        return PopulationCenterSerializer(population_centers, many=True).data

    @staticmethod
    def get_by_id(id):
        population_center = PopulationCenterRepository.get_by_id(id)
        return PopulationCenterSerializer(population_center).data

    @staticmethod
    def get_by_code(code):
        population_center = PopulationCenterRepository.get_by_code(code)
        return PopulationCenterSerializer(population_center).data

    @staticmethod
    def save(population_center_data):
        population_center = PopulationCenterRepository.save(population_center_data)
        return PopulationCenterSerializer(population_center).data

    @staticmethod
    def get_all_by_district(district_id):
        population_centers = PopulationCenterRepository.get_all_by_district(district_id)
        return PopulationCenterSerializer(population_centers, many=True).data
