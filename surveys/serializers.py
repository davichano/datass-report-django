from rest_framework import serializers


class CSVUploadSerializer(serializers.Serializer):
    ds_i = serializers.FileField(required=True)
    ds_ii = serializers.FileField(required=True)
    ds_iii = serializers.FileField(required=True)
    year = serializers.IntegerField(required=True)
    month = serializers.IntegerField(required=True)
