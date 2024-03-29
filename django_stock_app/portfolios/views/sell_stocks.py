from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse
from django.views.generic import UpdateView
from portfolios.forms.sell_stock_portfolio_form import SellStockPortfolioForm
from portfolios.models.portfolio_model import Portfolio
from portfolios.models.portfolio_stocks_model import PortfolioStocks
from stocks.models.companies import StockCompanies
from stocks.models.stock_prices import StockPrices

TODAY_DATE = settings.TODAY


def load_data(request):
    """Frontend function that returns detailed data about selected company."""
    ticker = request.GET.get("stock")
    company_full_name = StockCompanies.objects.filter(
        company_abbreviation=ticker
    ).first()
    last_stock_price = StockPrices.objects.filter(
        Q(company_abbreviation__company_abbreviation=ticker)
        & Q(date__contains=TODAY_DATE)
    ).first()
    return JsonResponse(
        {
            "company_name": company_full_name.company_full_name,
            "last_stock_price": last_stock_price.close_price,
        }
    )


class SellStockPortfolio(LoginRequiredMixin, UpdateView):
    model = PortfolioStocks
    form_class = SellStockPortfolioForm
    template_name = "portfolios/sell_stock_portfolio.html"
    slug_url_kwarg = "portfolio"
    slug_field = "portfolio_id"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None, *args, **kwargs):
        portfolio_id = (
            f"{self.request.user.username}_{self.kwargs.get(self.slug_url_kwarg)}"
        )
        stock_name = self.request.POST.get("stock")
        return self.model.objects.filter(
            Q(portfolio_id=portfolio_id) & Q(stock=stock_name)
        ).first()

    def get_context_data(self, **kwargs):
        context = {}
        context["form"] = self.get_form()
        context["portfolios"] = Portfolio.objects.filter(
            user__username=self.request.user.username
        ).all()
        return context

    def get_form_kwargs(self):
        kwargs = super(SellStockPortfolio, self).get_form_kwargs()
        kwargs["portfolio_id"] = (
            self.request.user.username + "_" + self.kwargs.get(self.slug_url_kwarg)
        )
        return kwargs

    def form_valid(self, form, **kwargs):
        portfolio_id = self.object.portfolio_id.portfolio_id
        stock_name = form.instance.stock
        queryset = self.model.objects.get(
            Q(portfolio_id=portfolio_id) & Q(stock=stock_name)
        )
        self.balance_update(
            form.instance.amount, form.instance.stock_price, portfolio_id
        )
        form.instance.amount = queryset.amount - form.instance.amount

        if form.instance.amount == 0:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "portfolio-detail",
            kwargs={"portfolio": self.kwargs.get(self.slug_url_kwarg)},
        )

    def balance_update(self, amount, stock_price, portfolio_id):
        """Update portfolio balance after stock selling."""
        queryset = Portfolio.objects.filter(portfolio_id=portfolio_id)
        current_balance: float = queryset.first().balance
        new_balance: float = current_balance + amount * stock_price
        queryset.update(balance=new_balance)
