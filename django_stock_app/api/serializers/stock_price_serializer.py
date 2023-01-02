from rest_framework import serializers
from stocks.models.stock_prices_model import StockPrices


class StockPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrices
        fields = '__all__'

