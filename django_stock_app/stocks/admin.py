from django.contrib import admin

from stocks.models.companies_model import StockCompanies
from stocks.models.stock_prices_model import StockPrices
# Register your models here.

admin.site.register(StockCompanies)
admin.site.register(StockPrices)
# Register your models here.
