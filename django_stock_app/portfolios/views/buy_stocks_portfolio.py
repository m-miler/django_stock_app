from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolios.models.portfolio_stocks_model import PortfolioStocks
from portfolios.forms.buy_stock_portfolio_form import BuyStockPortfolioForm, STOCK_CHOICES
from portfolios.models.portfolio_model import Portfolio
from stocks.models.companies_model import StockCompanies
from stocks.models.stock_prices_model import StockPrices
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import reverse


TODAY_DATE = '2022-12-29'


def load_data(request):
    ticker = request.GET.get('stock')
    company_full_name = StockCompanies.objects.filter(company_abbreviation=ticker).first()
    last_stock_price = StockPrices.objects.filter(Q(company_abbreviation__company_abbreviation=ticker) &
                                                  Q(date__contains=TODAY_DATE)).first()
    return JsonResponse({'company_name': company_full_name.company_full_name,
                         'last_stock_price': last_stock_price.close_price})


class BuyStockPortfolio(LoginRequiredMixin, UpdateView):
    model = PortfolioStocks
    form_class = BuyStockPortfolioForm
    template_name = 'portfolios/buy_stock_portfolio.html'
    slug_url_kwarg = 'portfolio'
    slug_field = 'portfolio_id'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None, *args, **kwargs):
        portfolio_id = self.request.user.username + '_' + self.kwargs.get(self.slug_url_kwarg)
        stock_name = STOCK_CHOICES[int(self.request.POST.get('stock'))-1]

        obj, created = PortfolioStocks.objects.filter(Q(portfolio_id=portfolio_id) &
                                                      Q(stock=stock_name)).get_or_create(
            defaults={'portfolio_id': Portfolio.objects.get(portfolio_id=portfolio_id),
                      'stock': stock_name,
                      'amount': 0,
                      'stock_price': 0})
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.get_form()
        context['portfolios'] = Portfolio.objects.filter(user__username=self.request.user.username).all()
        return context

    def form_valid(self, form, **kwargs):
        portfolio_id = self.request.user.username + '_' + self.kwargs.get(self.slug_url_kwarg)
        stock_name = form.instance.stock
        self.balance_update(form.instance.amount, form.instance.stock_price, portfolio_id)

        try:
            queryset = PortfolioStocks.objects.filter(Q(portfolio_id=portfolio_id) &
                                                      Q(stock=stock_name)).first()
        except:
            queryset = None

        form.instance.portfolio_id = Portfolio.objects.filter(portfolio_id=portfolio_id).first()
        form.instance.amount = form.instance.amount + queryset.amount

        if queryset is not None and queryset.stock_price != 0:
            form.instance.stock_price = (form.instance.stock_price + queryset.stock_price)/2

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('portfolio-detail', kwargs={'portfolio': self.kwargs.get(self.slug_url_kwarg)})

    def balance_update(self, amount, stock_price, portfolio_id):
        queryset = Portfolio.objects.filter(portfolio_id=portfolio_id)
        current_balance = queryset.first().balance
        new_balance = current_balance - amount * stock_price
        queryset.update(balance=new_balance)
