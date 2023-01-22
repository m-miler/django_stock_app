from django.contrib import admin

from .models.companies_model import StockCompanies
from .models.stock_prices_model import StockPrices

admin.site.register(StockCompanies)
admin.site.register(StockPrices)
