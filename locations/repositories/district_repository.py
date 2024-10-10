from locations.models import District


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
