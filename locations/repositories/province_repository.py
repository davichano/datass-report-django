from locations.models import Province
from django.db.models import Sum, F, FloatField, ExpressionWrapper, Case, When


class ProvinceRepository:
    @staticmethod
    def get_all():
        return Province.objects.all()

    @staticmethod
    def get_by_name(name):
        try:
            return Province.objects.get(name=name)
        except Province.DoesNotExist:
            return Province()

    @staticmethod
    def save(province_instance):
        province_instance.save()
        return province_instance

    @staticmethod
    def get_by_id(id):
        try:
            return Province.objects.get(id=id)
        except Province.DoesNotExist:
            return Province()

    @staticmethod
    def get_water_access_for_all_provinces(year, month):
        return (
            Province.objects.filter(
                districts__population_centers__dataset_i_records__year=year,
                districts__population_centers__dataset_i_records__month=month,
            )
            .annotate(
                total_population=Sum("districts__population_centers__dataset_i_records__total_population"),
                total_population_with_water=Sum(
                    "districts__population_centers__dataset_i_records__population_with_water"
                ),
                percentage_with_water=ExpressionWrapper(
                    F("total_population_with_water") * 100 / F("total_population"),
                    output_field=FloatField(),
                ),
            )
            .values("name", "total_population", "total_population_with_water", "percentage_with_water")
        )

    @staticmethod
    def get_ubs_access_for_all_provinces(year, month):
        return (
            Province.objects.filter(
                districts__population_centers__dataset_i_records__year=year,
                districts__population_centers__dataset_i_records__month=month,
            )
            .annotate(
                total_population=Sum("districts__population_centers__dataset_i_records__total_population"),
                total_population_with_ubs=Sum(
                    Case(
                        When(
                            districts__population_centers__dataset_i_records__has_sanitation_system=True,
                            then=F("districts__population_centers__dataset_i_records__total_population"),
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
