# locations/repositories/district_repository.py
from locations.models import District
from django.db.models import Sum, F, FloatField, ExpressionWrapper, Case, When


class DistrictRepository:
    @staticmethod
    def get_all():
        return District.objects.all()

    @staticmethod
    def get_by_name(name):
        try:
            return District.objects.get(name=name)
        except District.DoesNotExist:
            return District()

    @staticmethod
    def get_by_id(district_id):
        try:
            return District.objects.get(id=district_id)
        except District.DoesNotExist:
            return District()

    @staticmethod
    def save(district_instance):
        district_instance.save()
        return district_instance

    @staticmethod
    def get_by_province(province):
        return District.objects.filter(province=province)

    @staticmethod
    def get_water_access_by_province(province_id, year, month):
        return (
            District.objects.filter(
                population_centers__dataset_i_records__year=year,
                population_centers__dataset_i_records__month=month,
                province_id=province_id,
            )
            .annotate(
                total_population=Sum("population_centers__dataset_i_records__total_population"),
                total_population_with_water=Sum(
                    "population_centers__dataset_i_records__population_with_water"
                ),
                percentage_with_water=ExpressionWrapper(
                    F("total_population_with_water") * 100 / F("total_population"),
                    output_field=FloatField(),
                ),
            )
            .values("name", "total_population", "total_population_with_water", "percentage_with_water")
        )

    @staticmethod
    def get_ubs_access_by_province(province_id, year, month):
        return (
            District.objects.filter(
                population_centers__dataset_i_records__year=year,
                population_centers__dataset_i_records__month=month,
                province_id=province_id,
            )
            .annotate(
                total_population=Sum("population_centers__dataset_i_records__total_population"),
                total_population_with_ubs=Sum(
                    Case(
                        When(
                            population_centers__dataset_i_records__has_sanitation_system=True,
                            then=F("population_centers__dataset_i_records__total_population"),
                        ),
                        default=0,
                        output_field=FloatField(),
                    )
                ),
                percentage_with_ubs=ExpressionWrapper(
                    F("total_population_with_ubs") * 100 / F("total_population"),
                    output_field=FloatField(),
                ),
            )
            .values("name", "total_population", "total_population_with_ubs", "percentage_with_ubs")
        )
