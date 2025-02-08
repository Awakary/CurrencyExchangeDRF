from decimal import Decimal

from django.core.management import BaseCommand

from api.models import ExchangeRate, Currency


class Command(BaseCommand):

    help = 'Filling database'

    def handle(self, *args, **options):
        currencies = [('Австралийский доллар', 'AUD', '$'),
                      ('Гуарани', 'PYG', '₲'),
                      ('Иена', 'JPY', '¥')]
        currency_ids = []
        for currency in currencies:
            currency = Currency.objects.get_or_create(name=currency[0], code=currency[1], sign=currency[2])
            currency_ids.append(currency[0].id)
        for i in range(len(currency_ids) - 1):
            ExchangeRate.objects.update_or_create(base_currency_id=currency_ids[i],
                                                  target_currency_id=currency_ids[i + 1],
                                                  defaults={"rate": Decimal(i+0.252525)}
                                                  )
        print('База заполнена')
