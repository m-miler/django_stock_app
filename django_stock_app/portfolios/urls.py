from django.urls import path
from portfolios.views.create_portfolio import CreatePortfolio
from portfolios.views.detail_portfolio import PortfolioDetailed
from portfolios.views.buy_stocks_portfolio import BuyStockPortfolio, load_data
from portfolios.views.delete_portfolio import DeletePortfolio

urlpatterns = [
    path('create', CreatePortfolio.as_view(), name='portfolio-create'),
    path('<str:portfolio>', PortfolioDetailed.as_view(), name='portfolio-detail'),
    path('<str:portfolio>/buy', BuyStockPortfolio.as_view(), name='portfolio-buy'),
    path('delete/<str:portfolio>', DeletePortfolio.as_view(), name='portfolio-delete'),
    path('ajax/load_data', load_data, name='ajax-load-data')
]
