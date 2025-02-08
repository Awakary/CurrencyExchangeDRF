from django.contrib import admin

from api.models import Currency, ExchangeRate


class BaseCurrencyInline(admin.StackedInline):
    model = ExchangeRate
    fk_name = 'base_currency'
    extra = 1


class TargetCurrencyInline(admin.StackedInline):
    model = ExchangeRate
    fk_name = 'target_currency'
    extra = 1


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('id', 'code', 'name')
    inlines = [BaseCurrencyInline, TargetCurrencyInline]


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'base_currency', 'target_currency')
    search_fields = ('id', 'base_currency', 'target_currency')
