# surveys/repositories/dataset_i_repository.py
from django.db.models import Sum

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

    @staticmethod
    def get_last_year_month():
        return DatasetI.objects.order_by("-year", "-month").first()

    @staticmethod
    def get_totals_by_year_month(year, month):
        data = DatasetI.objects.filter(year=year, month=month).aggregate(
            total_people=Sum("total_population"),
            total_people_with_water=Sum("population_with_water"),
            total_houses=Sum("inhabited_houses"),
            total_houses_with_connection=Sum("total_houses_with_connection"),
        )

        return data

    @staticmethod
    def get_totals_by_year_month_province(year, month, province):
        data = DatasetI.objects.filter(
            year=year, month=month, population_center__district__province_id=province
        ).aggregate(
            total_people=Sum("total_population"),
            total_people_with_water=Sum("population_with_water"),
            total_houses=Sum("inhabited_houses"),
            total_houses_with_connection=Sum("total_houses_with_connection"),
        )

        return data
