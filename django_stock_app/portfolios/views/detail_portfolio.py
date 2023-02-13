from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from portfolios.charts.portfolio_charts import portfolio_chart
from portfolios.models.portfolio_model import Portfolio
from portfolios.models.portfolio_stocks_model import PortfolioStocks


class PortfolioDetailed(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = "portfolios/portfolio.html"
    slug_field = "name"
    slug_url_kwarg = "portfolio"

    def get_object(self, queryset=None, *args, **kwargs):
        portfolio_id = (
            f"{self.request.user.username}_{self.kwargs.get(self.slug_url_kwarg)}"
        )
        return self.model.objects.filter(portfolio_id=portfolio_id).first()

    def get_context_data(self, **kwargs):
        portfolio_id = f"{self.request.user.username}_{self.kwargs.get('portfolio')}"
        portfolio_stocks_queryset = PortfolioStocks.objects.filter(
            portfolio_id=portfolio_id
        ).all()
        portfolios = self.model.objects.filter(user=self.request.user).all()
        portfolio_detail = self.model.objects.filter(
            portfolio_id=portfolio_id, user=self.request.user
        ).first()

        context = {}
        context["portfolios"] = portfolios
        context["portfolio_detail"] = portfolio_detail
        context["portfolio_stocks"] = portfolio_stocks_queryset
        context["totals"] = self.get_totals(
            portfolio_stocks_queryset, portfolio_detail.balance
        )
        context["chart"] = portfolio_chart(portfolio_stocks_queryset)
        return context

    def get_totals(self, queryset, balance) -> dict:
        total_pricing: float = sum([stock.pricing for stock in queryset])
        total_portfolio_pricing: float = sum(
            [stock.portfolio_pricing for stock in queryset]
        )
        total_profit_loss: float = sum([stock.profit_loss for stock in queryset])
        total: float = total_pricing + balance
        total_profit_loss_percentage: float = round(
            total_profit_loss / total_portfolio_pricing * 100
            if total_portfolio_pricing > 0
            else 0,
            2,
        )
        return {
            "total_pricing": total_pricing,
            "total_portfolio_pricing": total_portfolio_pricing,
            "total_profit_loss": total_profit_loss,
            "total_profit_loss_percentage": total_profit_loss_percentage,
            "total": total,
        }
