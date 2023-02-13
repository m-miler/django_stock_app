from django.contrib import admin

from .models.portfolio_model import Portfolio
from .models.portfolio_stocks_model import PortfolioStocks

admin.site.register(Portfolio)
admin.site.register(PortfolioStocks)
