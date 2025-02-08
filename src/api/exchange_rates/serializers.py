from django.db import IntegrityError
from rest_framework import serializers

from api.currencies.serializers import CurrencySerializer
from api.models import Currency, ExchangeRate
from api.utils import CustomErrorSerializer


class ExchangeRatePathSerializer(CustomErrorSerializer):
    double_code = serializers.CharField(required=True, min_length=6, max_length=6)


class ExchangeRateSerializer(CustomErrorSerializer, serializers.ModelSerializer):
    baseCurrencyCode = serializers.SlugRelatedField(slug_field='code', write_only=True,
                                                    queryset=Currency.objects.all())
    targetCurrencyCode = serializers.SlugRelatedField(slug_field='code', write_only=True,
                                                      queryset=Currency.objects.all())
    baseCurrency = CurrencySerializer(source="base_currency", read_only=True)
    targetCurrency = CurrencySerializer(source="target_currency", read_only=True)

    def create(self, validated_data):
        try:
            return ExchangeRate.objects.create(
                base_currency=validated_data['baseCurrencyCode'],
                target_currency=validated_data['targetCurrencyCode'],
                rate=validated_data['rate']
            )
        except IntegrityError:
            raise serializers.ValidationError({"message": "Валютная пара с таким кодом уже существует"})

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["rate"] = round(float(representation["rate"]), 2)
        return representation

    class Meta:
        model = ExchangeRate
        exclude = ["base_currency", "target_currency"]
