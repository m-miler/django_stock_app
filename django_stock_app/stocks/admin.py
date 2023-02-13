from django.contrib import admin

from .models.companies import StockCompanies
from .models.stock_prices import StockPrices

admin.site.register(StockCompanies)
admin.site.register(StockPrices)
