from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from api.models import ExchangeRate


class ExchangeServiceApiTestCase(TestCase):
    fixtures = ['tests/fixtures/currencies.json',
                'tests/fixtures/exchange_rates.json']

    def setUp(self) -> None:
        super().setUp()
        self.prev_exchange_rates_count = ExchangeRate.objects.count()

    def test_get_converted_amount_by_normal(self):
        url = "{0}?from={1}&to={2}&amount={3}".format(reverse("converted_amount"),
                                                      "PYG", "AUD", 10)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["convertedAmount"], 12.5)

    def test_get_converted_amount_by_reverse(self):
        url = "{0}?from={1}&to={2}&amount={3}".format(reverse("converted_amount"),
                                                      "PYG", "JPY", 7)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["convertedAmount"], 3.32)

    def test_get_converted_amount_by_cross(self):
        url = "{0}?from={1}&to={2}&amount={3}".format(reverse("converted_amount"),
                                                      "USD", "JPY", 11)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["convertedAmount"], 7.43)

    def test_get_converted_amount_not_found(self):
        url = "{0}?from={1}&to={2}&amount={3}".format(reverse("converted_amount"),
                                                      "AUD", "USD", 8)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_converted_amount_with_bad_request(self):
        url = "{0}?from={1}&to={2}&amount={3}".format(reverse("converted_amount"),
                                                      "aaaa", "bbbb", 9)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_converted_amount_with_bad_request_short(self):
        url = "{0}?from={1}&to={2}&amount={3}".format(reverse("converted_amount"),
                                                      "aa", "BB", 3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_converted_amount_with_bad_request_not_amount(self):
        url = "{0}?from={1}&to={2}&amount=".format(reverse("converted_amount"),
                                                   "AUD", "USD")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Поле: amount - Введите правильное число.")
