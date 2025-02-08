from rest_framework import serializers

from api.exchange_rates.serializers import ExchangeRateSerializer
from api.utils import CustomErrorSerializer


class ConvertedAmountPathSerializer(CustomErrorSerializer):
    _from = serializers.CharField(required=True, min_length=3, max_length=3)
    to = serializers.CharField(required=True, min_length=3, max_length=3)
    amount = serializers.IntegerField(required=True)


class ConvertedAmountSerializer(ExchangeRateSerializer):
    convertedAmount = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    def get_convertedAmount(self, obj):
        return self.context.get('convertedAmount')

    def get_amount(self, obj):
        return self.context.get('amount')
