from django.contrib import admin
from portfolios.models.portfolio_model import Portfolio
from portfolios.models.portfolio_stocks_model import PortfolioStocks

admin.site.register(Portfolio)
admin.site.register(PortfolioStocks)
