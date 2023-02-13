from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import reverse
from django.views.generic import UpdateView
from portfolios.forms.buy_stock_portfolio_form import (STOCK_CHOICES,
                                                       BuyStockPortfolioForm)
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


class BuyStockPortfolio(LoginRequiredMixin, UpdateView):
    """Buy Stock View."""

    model = PortfolioStocks
    form_class = BuyStockPortfolioForm
    template_name = "portfolios/buy_stock_portfolio.html"
    slug_url_kwarg = "portfolio"
    slug_field = "portfolio_id"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None, *args, **kwargs):
        portfolio_id = (
            f"{self.request.user.username}_{self.kwargs.get(self.slug_url_kwarg)}"
        )
        stock_name = self.request.POST.get("stock")
        return PortfolioStocks.objects.filter(
            Q(portfolio_id=portfolio_id) & Q(stock=stock_name)
        ).first()

    def get_form_kwargs(self):
        kwargs = super(BuyStockPortfolio, self).get_form_kwargs()
        portfolio_id = (
            f"{self.request.user.username}_{self.kwargs.get(self.slug_url_kwarg)}"
        )
        kwargs.update({"portfolio_id": portfolio_id})
        return kwargs

    def get_context_data(self, **kwargs):
        context = {}
        context["form"] = self.get_form()
        context["portfolios"] = Portfolio.objects.filter(
            user__username=self.request.user.username
        ).all()
        return context

    def form_valid(self, form, **kwargs):
        portfolio_id = (
            f"{self.request.user.username}_{self.kwargs.get(self.slug_url_kwarg)}"
        )
        if self.object is not None:
            stock_name = self.object.stock
            queryset = PortfolioStocks.objects.filter(
                Q(portfolio_id=portfolio_id) & Q(stock=stock_name)
            ).first()
            form.instance.portfolio_id = self.object.portfolio_id
            self.balance_update(
                form.instance.amount, form.instance.stock_price, portfolio_id
            )
            form.instance.amount = form.instance.amount + queryset.amount
            form.instance.stock_price = (
                form.instance.stock_price + queryset.stock_price
            ) / 2
        else:
            form.instance.portfolio_id = Portfolio.objects.get(
                portfolio_id=portfolio_id
            )
            self.balance_update(
                form.instance.amount, form.instance.stock_price, portfolio_id
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "portfolio-detail",
            kwargs={"portfolio": self.kwargs.get(self.slug_url_kwarg)},
        )

    def balance_update(self, amount, stock_price, portfolio_id):
        """Update portfolio balance after stock buying."""
        queryset = Portfolio.objects.filter(portfolio_id=portfolio_id)
        current_balance = queryset.first().balance
        new_balance = current_balance - amount * stock_price
        queryset.update(balance=new_balance)
