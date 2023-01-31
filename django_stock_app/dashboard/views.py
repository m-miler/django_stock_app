from django.conf import settings
from django.shortcuts import render, redirect
from stocks.models.stock_prices_model import StockPrices
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from dashboard.charts import stock_chart
from portfolios.models.portfolio_model import Portfolio
from twitter.views import search_tweets

TODAY_DATE = settings.TODAY
LAST_WEEK_END = settings.LAST_WEEK_END


def home(request):
    """
    Function checks if a user is logged in then render the home page, otherwise redirect to login page.
    """
    if request.user.username:
        portfolios = Portfolio.objects.filter(user__username=request.user.username).all().values('name')
        return render(request, 'dashboard/index.html', context={'portfolios': portfolios})
    else:
        return redirect('login')


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    Application basic view. Verify that the current user is authenticated.
    If user is authenticated render a templet based on stock/index in request.
    """
    def get_template_names(self):
        ticker: str = (self.kwargs.get('ticker')).upper()
        if ticker[:3] == 'WIG':
            return ['dashboard/wig.html']
        return ['dashboard/stock_detail.html']

    def get_context_data(self, **kwargs):
        ticker: str = (kwargs.get('ticker')).upper()
        queryset = StockPrices.objects.filter(company_abbreviation__index=ticker).all()
        chart_data = StockPrices.objects.filter(company_abbreviation__company_abbreviation=ticker).all()

        context = super(Dashboard, self).get_context_data(**kwargs)
        context['stock_price'] = chart_data.filter(Q(company_abbreviation__company_abbreviation=ticker) &
                                                   Q(date=TODAY_DATE)).first()

        context['companies'] = queryset.filter(date=TODAY_DATE)
        context['top_companies'] = queryset.filter(date=TODAY_DATE).order_by('-close_price')[:5]
        context['chart'] = stock_chart(chart_data)
        context['ticker'] = ticker
        context['portfolios'] = Portfolio.objects.filter(user__username=self.request.user.username).all()

        if ticker[:3] != 'WIG':
            context['tweets'] = search_tweets(ticker)

        return context
