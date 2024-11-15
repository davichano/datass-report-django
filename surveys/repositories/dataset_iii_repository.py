from django.db.models import Count, Q, F, Case, When, FloatField, Sum

from surveys.models import DatasetIII


class DatasetIIIRepository:
    @staticmethod
    def bulk_create(instances):
        DatasetIII.objects.bulk_create(instances, batch_size=500)

    @staticmethod
    def get_last_year_month():
        return DatasetIII.objects.order_by("-year", "-month").first()

    @staticmethod
    def get_systems_resume(year, month):
        data = (
            DatasetIII.objects.filter(year=year, month=month)
            .values(
                "population_center__district__province__name",
                "population_center__district__province__id",
            )
            .annotate(
                total_systems=Count("id"),
                total_with_continous_water=Count("id", filter=Q(continuous_water_service=True)),
                percent_with_continous_water=Case(
                    When(total_systems=0, then=0),  # Evita división por cero
                    default=(F("total_with_continous_water") * 1.0 / F("total_systems")),
                    output_field=FloatField(),
                ),
                total_with_clorination=Count("id", filter=Q(has_chlorination_system=True)),
                total_makes_clorination=Count("id", filter=Q(chlorinates_water=True)),
                total_people_served=Sum(
                    "served_population_with_connection", filter=Q(served_population_with_connection__gt=0)
                ),
                total_people_served_with_clorination=Sum(
                    "served_population_with_connection", filter=Q(chlorinates_water=True)
                ),
            )
        ).order_by("population_center__district__province__name")
        return data

    @staticmethod
    def get_total_by_state(year, month):
        return (
            DatasetIII.objects.filter(year=year, month=month)
            .values("operational_state_annual")
            .annotate(total=Count("operational_state_annual"))
            .order_by("-total")
        )

    @staticmethod
    def get_total_by_type(year, month):
        return (
            DatasetIII.objects.filter(year=year, month=month)
            .values("water_system_type")
            .annotate(total=Count("water_system_type"))
            .order_by("-total")
        )
