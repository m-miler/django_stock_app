from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from api.serializers.stock_price_serializer import StockPricesSerializer
from stocks.models.stock_prices_model import StockPrices


class StockPricesViewSet(ListModelMixin, GenericViewSet):
    queryset = StockPrices.objects.all()
    serializer_class = StockPricesSerializer
    filterset_fields = ['company_abbreviation', 'date']




