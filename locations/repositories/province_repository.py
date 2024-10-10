from locations.models import Province


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
