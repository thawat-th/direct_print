from rest_framework import serializers

from api.models import Print, Printer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = "__all__"


class PrintFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = "__all__"
