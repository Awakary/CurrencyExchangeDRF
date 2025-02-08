import json

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from api.models import ExchangeRate


class ExchangeRateApiTestCase(TestCase):

    fixtures = ['tests/fixtures/currencies.json',
                'tests/fixtures/exchange_rates.json']

    def setUp(self) -> None:
        super().setUp()
        self.prev_exchange_rates_count = ExchangeRate.objects.count()

    def test_get_exchange_rate(self):
        url = reverse("exchange_rate", kwargs={"double_code": "PYGAUD"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["rate"], 1.25)

    def test_get_exchange_rate_not_found(self):
        url = reverse("exchange_rate", kwargs={"double_code": "PYGAU1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "Обменный курс для пары не найден")

    def test_get_exchange_rate_bad_double_code(self):
        url = reverse("exchange_rate", kwargs={"double_code": "PYGAUD1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Поле: double_code - Убедитесь, что это "
                                                     "значение содержит не более 6 символов.")

    def test_get_exchange_rate_bad_double_code_len(self):
        url = reverse("exchange_rate", kwargs={"double_code": "PYGAU"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Поле: double_code - Убедитесь, что это "
                                                     "значение содержит не менее 6 символов.")

    def test_get_exchange_rates(self):
        url = reverse("exchange_rates-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), ExchangeRate.objects.count())

    def test_create_exchange_rate(self):
        url = reverse("exchange_rates-list")
        data = {
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "EUR",
            "rate": 0.99
            }
        response = self.client.post(url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeRate.objects.count(), self.prev_exchange_rates_count + 1)

    def test_update_exchange_rate(self):
        exc_change = ExchangeRate.objects.filter(base_currency__code="PYG",
                                                 target_currency__code="AUD").first()
        self.assertNotEqual(exc_change.rate, 1.05)
        url = reverse("exchange_rate", kwargs={"double_code": "PYGAUD"})
        response = self.client.patch(url, data=json.dumps({"rate": 1.05}),
                                     content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["rate"], 1.05)

    def test_create_exchange_rate_with_bad_request(self):
        url = reverse("exchange_rates-list")
        data = {
            "baseCurrencyCode": "USD",
            "rate": 0.99
            }
        response = self.client.post(url, data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
