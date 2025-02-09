from rest_framework import serializers
from api.models import Currency
from api.utils import CustomErrorSerializer


class CurrencyPathSerializer(CustomErrorSerializer):
    code = serializers.CharField(required=True, min_length=3, max_length=3)


class CurrencySerializer(CustomErrorSerializer, serializers.ModelSerializer):
    def validate_code(self, value):
        if Currency.objects.filter(code=value.upper()).exists():
            raise serializers.ValidationError("Валюта с таким кодом уже существует")
        return value

    class Meta:
        model = Currency
        fields = "__all__"
