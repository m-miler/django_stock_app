from django.urls import path
from portfolios.views.create_portfolio import CreatePortfolio
from portfolios.views.detail_portfolio import PortfolioDetailed

urlpatterns = [
    path('create', CreatePortfolio.as_view(), name='portfolio-create'),
    path('<str:portfolio>', PortfolioDetailed.as_view(), name='portfolio-detail')
]
