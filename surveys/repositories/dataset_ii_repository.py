from surveys.models import DatasetII


class DatasetIIRepository:
    @staticmethod
    def bulk_create(instances):
        DatasetII.objects.bulk_create(instances, batch_size=500)
