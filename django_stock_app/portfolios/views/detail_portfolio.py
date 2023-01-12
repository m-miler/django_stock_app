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

    def get_object(self, queryset=None, *args, **kwargs):
        portfolio_id = self.request.user.username + '_' + self.kwargs.get(self.slug_url_kwarg)
        obj = Portfolio.objects.filter(portfolio_id=portfolio_id).first()
        return obj

    def get_context_data(self, **kwargs):
        portfolio_id = self.request.user.username + '_' + self.kwargs.get('portfolio')
        portfolio_stocks_queryset = PortfolioStocks.objects.filter(portfolio_id=portfolio_id).all()

        context = super(PortfolioDetailed, self).get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.filter(user__username=self.request.user.username).all()
        context['portfolio_detail'] = Portfolio.objects.filter(portfolio_id=portfolio_id).first()
        context['portfolio_stocks'] = portfolio_stocks_queryset
        context['totals'] = self.get_totals(portfolio_stocks_queryset, portfolio_id)
        context['chart'] = portfolio_chart(portfolio_stocks_queryset)
        return context

    def get_totals(self, queryset, portfolio_id):
        total_pricing = sum([stock.pricing for stock in queryset])
        total_portfolio_pricing = sum([stock.portfolio_pricing for stock in queryset])
        total_profit_loss = sum([stock.profit_loss for stock in queryset])
        total = total_pricing + Portfolio.objects.filter(portfolio_id=portfolio_id).first().balance
        if total_portfolio_pricing > 0:
            total_profit_loss_percentage = round(total_profit_loss / total_portfolio_pricing, 2) * 100
        else:
            total_profit_loss_percentage = 0
        context_dict = {'total_pricing': total_pricing,
                        'total_portfolio_pricing': total_portfolio_pricing,
                        'total_profit_loss': total_profit_loss,
                        'total_profit_loss_percentage': total_profit_loss_percentage,
                        'total': total
                        }
        return context_dict
