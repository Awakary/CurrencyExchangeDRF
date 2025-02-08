from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from api.converted_service.serializers import ConvertedAmountPathSerializer
from api.converted_service.service import ConvertedAmountService


class ConvertedAmountView(APIView):
    def get(self, request):
        query_params = request.query_params.copy()
        query_params["_from"] = query_params.get('from')
        serializer = ConvertedAmountPathSerializer(data=query_params)
        if serializer.is_valid():
            from_currency = serializer.validated_data['_from']
            to_currency = serializer.validated_data['to']
            amount = serializer.validated_data['amount']
            exchange = ConvertedAmountService(from_currency, to_currency, amount).get_exchange()
            if exchange:
                return Response(exchange.data)
            else:
                return Response({"message": "Валютная пара отсутствует в базе данных"},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
