from django.urls import path

from .views.buy_stocks import BuyStockPortfolio, load_data
from .views.create_portfolio import CreatePortfolio
from .views.delete_portfolio import DeletePortfolio
from .views.detail_portfolio import PortfolioDetailed
from .views.sell_stocks import SellStockPortfolio

urlpatterns = [
    path("create", CreatePortfolio.as_view(), name="portfolio-create"),
    path("<str:portfolio>", PortfolioDetailed.as_view(), name="portfolio-detail"),
    path("<str:portfolio>/buy", BuyStockPortfolio.as_view(), name="portfolio-buy"),
    path("<str:portfolio>/sell", SellStockPortfolio.as_view(), name="portfolio-sell"),
    path("delete/<str:portfolio>", DeletePortfolio.as_view(), name="portfolio-delete"),
    path("ajax/load_data", load_data, name="ajax-load-data"),
]
