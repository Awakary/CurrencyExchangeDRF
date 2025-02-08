from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from api.converted_service.views import ConvertedAmountView
from api.currencies.views import CurrencyViewSet
from api.exchange_rates.views import ExchangeRateViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Exchange API",
      default_version='v1',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path(r"exchange", ConvertedAmountView.as_view(),  name='converted_amount'),
   path(r"currency/<str:code>", CurrencyViewSet.as_view({"get": "retrieve"}), name='currency'),
   path(r"exchangeRate/<slug:double_code>", ExchangeRateViewSet.as_view({"get": "retrieve",
                                                                         "patch": "partial_update"}),
        name='exchange_rate'),
]
router = routers.SimpleRouter(trailing_slash=False)

router.register("exchangeRates", ExchangeRateViewSet, basename="exchange_rates")
router.register("currencies", CurrencyViewSet, basename="currencies")


urlpatterns += router.urls
