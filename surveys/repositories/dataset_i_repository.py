# surveys/repositories/dataset_i_repository.py
from surveys.models import DatasetI


class DatasetIRepository:
    @staticmethod
    def get_all():
        return DatasetI.objects.all()

    @staticmethod
    def get_by_population_center(name):
        return DatasetI.objects.filter(population_center=name)

    @staticmethod
    def save(dataset_instance):
        dataset_instance.save()

    @staticmethod
    def bulk_create(instances):
        DatasetI.objects.bulk_create(instances, batch_size=500)  # Ajustar el tamaño de batch si es necesario
