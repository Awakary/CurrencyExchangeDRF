from django.db.models import Q
from django.http import Http404

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.models import ExchangeRate
from api.exchange_rates.serializers import ExchangeRateSerializer, ExchangeRatePathSerializer


class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

    def get_object(self, *args, **kwargs):
        serializer = ExchangeRatePathSerializer(data=self.kwargs)
        if serializer.is_valid():
            double_code = serializer.validated_data["double_code"]
            instance = self.queryset.filter(Q(base_currency__code=double_code[:3]) &
                                            Q(target_currency__code=double_code[3:])).first()
            if instance:
                return instance
            raise Http404({"message": "Обменный курс для пары не найден"})
        raise ValidationError(serializer.errors)
