from django.http import Http404
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from api.currencies.serializers import CurrencySerializer, CurrencyPathSerializer
from api.models import Currency


class CurrencyViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_object(self, *args, **kwargs):
        serializer = CurrencyPathSerializer(data=self.kwargs)
        print(5)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            instance = self.queryset.filter(code=code).first()
            if instance:
                return instance
            raise Http404({"message": "Валюта не найдена"})
        raise ValidationError(serializer.errors)
