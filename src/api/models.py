from django.db import models


class Currency(models.Model):
    code = models.CharField(
        max_length=3,
        verbose_name="Код валюты",
        db_comment="Код валюты")
    name = models.CharField(
        max_length=128,
        verbose_name="Наименование валюты",
        db_comment="Наименование валюты")
    sign = models.CharField(
        max_length=16,
        verbose_name="Символ валюты",
        db_comment="Символ валюты")

    class Meta:
        verbose_name = "Валюта"
        db_table_comment = "Валюты"
        verbose_name_plural = "Валюты"
        db_table = '"course"."currency"'
        constraints = [
            models.UniqueConstraint(fields=["code"], name="iu_currency$code"),
        ]
        indexes = [
            models.Index(fields=["code"], name="ix_currency$code")
        ]

    def __str__(self):
        return f"{self.code} ({self.name})"


class ExchangeRate(models.Model):
    base_currency = models.ForeignKey(
        Currency,
        verbose_name="Базовая валюта",
        db_comment="Базовая валюта",
        on_delete=models.CASCADE,
        related_name="base_currencies",
        db_constraint=False,
        db_index=False)
    target_currency = models.ForeignKey(
        Currency,
        verbose_name="Целевая валюта",
        db_comment="Целевая валюта",
        on_delete=models.CASCADE,
        related_name="target_currencies",
        db_constraint=False,
        db_index=False)
    rate = models.DecimalField(
        decimal_places=6,
        max_digits=15,
        verbose_name="Курс обмена единицы базовой валюты к единице целевой валюты",
        db_comment="Курс обмена единицы базовой валюты к единице целевой валюты")

    class Meta:
        verbose_name = "Курс обмена"
        db_table_comment = "Курсы обмена"
        verbose_name_plural = "Курсы обмена"
        db_table = '"course"."exchange_rate"'
        constraints = [
            models.UniqueConstraint(fields=["base_currency", "target_currency"],
                                    name="iu_base_currency_id$target_currency_id"),
        ]
        indexes = [
            models.Index(fields=["base_currency", "target_currency"],
                         name="ix_base_cur$target_cur"),
        ]

    def __str__(self):
        return f"{self.base_currency.code} к {self.target_currency.code}"
