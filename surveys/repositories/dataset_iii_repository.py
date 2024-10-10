from surveys.models import DatasetIII


class DatasetIIIRepository:
    @staticmethod
    def bulk_create(instances):
        DatasetIII.objects.bulk_create(instances, batch_size=500)
