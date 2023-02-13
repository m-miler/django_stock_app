from api.serializers.stock_price_serializer import StockPricesSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from stocks.models.stock_prices import StockPrices


class StockPricesViewSet(ListModelMixin, GenericViewSet):
    queryset = StockPrices.objects.all()
    serializer_class = StockPricesSerializer
    filterset_fields = ["company_abbreviation", "date"]
