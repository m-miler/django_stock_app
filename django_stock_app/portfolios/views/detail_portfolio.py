from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolios.models.portfolio_model import Portfolio
from portfolios.models.portfolio_stocks_model import PortfolioStocks
from portfolios.charts.portfolio_charts import portfolio_chart


class PortfolioDetailed(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'portfolios/portfolio.html'
    slug_field = 'name'
    slug_url_kwarg = 'portfolio'

    def get_context_data(self, **kwargs):
        portfolio_id = self.request.user.username + '_' + self.kwargs.get('portfolio')
        portfolio_stocks_queryset = PortfolioStocks.objects.filter(portfolio_id=portfolio_id).all()

        context = super(PortfolioDetailed, self).get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.filter(user__username=self.request.user.username).all()
        context['portfolio_detail'] = Portfolio.objects.filter(portfolio_id=portfolio_id).first()
        context['portfolio_stocks'] = portfolio_stocks_queryset
        context['chart'] = portfolio_chart(portfolio_stocks_queryset)
        return context
