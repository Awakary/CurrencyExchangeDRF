from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from api.models import Currency


class CurrencyApiTestCase(TestCase):

    fixtures = ['tests/fixtures/currencies.json']

    def setUp(self) -> None:
        super().setUp()
        self.prev_currencies_count = Currency.objects.count()

    def test_get_currency(self):
        url = reverse("currency", kwargs={"code": "EUR"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["code"], "EUR")

    def test_get_currency_not_found(self):
        url = reverse("currency", kwargs={"code": "EU1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_currency_not_correct_code(self):
        url = reverse("currency", kwargs={"code": "EU"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Поле: code - Убедитесь,"
                                                     " что это значение содержит не менее 3 символов.")

    def test_get_currencies(self):
        url = reverse("currencies-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Currency.objects.count())

    def test_create_currency(self):
        url = reverse("currencies-list")
        data = {
                "name": "Auro",
                "code": "AUR",
                "sign": "%"
            }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.count(), self.prev_currencies_count + 1)

    def test_create_currency_with_bad_request(self):
        url = reverse("currencies-list")
        data = {
                "name": "Auro",
                "code": "AUR",
            }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
