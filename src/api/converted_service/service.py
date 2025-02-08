from decimal import Decimal

from django.db.models import Q

from api.converted_service.serializers import ConvertedAmountSerializer
from api.models import ExchangeRate


class ConvertedAmountService:
    """Сервис для конвертации валют"""

    def __init__(self, from_currency, to_currency, amount):
        self.base = from_currency
        self.target = to_currency
        self.amount = amount
        self.queryset = ExchangeRate.objects.all()

    def get_exchange(self) -> ConvertedAmountSerializer:

        """Функция получения метода расчета курса"""

        instance = self.queryset.filter(Q(base_currency__code=self.base) &
                                        Q(target_currency__code=self.target)).first()
        if instance:
            return self.get_by_normal_rate(instance)

        instance = self.queryset.filter(Q(base_currency__code=self.target) &
                                        Q(target_currency__code=self.base)).first()
        if instance:
            return self.get_by_reverse_rate(instance)
        bases_for_search = self.queryset.filter(Q(target_currency__code=self.base))
        targets_for_search = self.queryset.filter(Q(target_currency__code=self.target))
        if bases_for_search and targets_for_search:
            return self.get_by_cross_rate(bases_for_search, targets_for_search)

    def get_by_normal_rate(self, instance) -> ConvertedAmountSerializer:

        """Функция расчета по обычному курсу"""

        converted_amount = (Decimal(self.amount) * Decimal(instance.rate)).quantize(Decimal("1.00"))
        return ConvertedAmountSerializer(instance, context={"amount": self.amount,
                                                            "convertedAmount": converted_amount})

    def get_by_reverse_rate(self, instance) -> ConvertedAmountSerializer:

        """Функция расчета по обратному курсу"""

        converted_amount = (Decimal(self.amount) * 1 / Decimal(instance.rate)).quantize(Decimal("1.00"))
        return ConvertedAmountSerializer(instance, context={"amount": self.amount,
                                                            "convertedAmount": converted_amount})

    def get_by_cross_rate(self, bases, targets) -> ConvertedAmountSerializer:

        """Функция расчета по кросс-курсу"""

        for i in bases:
            for j in targets:
                if i.base_currency.code == j.base_currency.code:
                    cross_rate = Decimal(i.rate) / Decimal(j.rate).quantize(Decimal("1.00"))
                    converted_amount = (Decimal(self.amount) * cross_rate).quantize(Decimal("1.00"))
                    data = {"base_currency": i.target_currency, "target_currency": j.target_currency,
                            "rate": cross_rate}
                    return ConvertedAmountSerializer(data, context={"amount": self.amount,
                                                                    "convertedAmount": converted_amount})
