# serializers.py
from rest_framework import serializers
from locations.models import PopulationCenter, Province, District


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class PopulationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopulationCenter
        fields = "__all__"
