from datetime import datetime, timedelta
from stocks.models.stock_prices_model import StockPrices
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from dashboard.charts import stock_chart

TODAY_DATE = (datetime.date(datetime.today()) - timedelta(days=1)).strftime('%Y-%m-%d')
LAST_WEEK_END = (datetime.date(datetime.today()) - timedelta(days=7)).strftime('%Y-%m-%d')


class Dashboard(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        ticker = (self.kwargs.get('ticker')).upper()
        if ticker[:3] == 'WIG':
            return ['dashboard/wig.html']
        else:
            return ['dashboard/stock_detail.html']

    def get_context_data(self, **kwargs):
        ticker = (kwargs.get('ticker')).upper()
        queryset = StockPrices.objects.filter(company_abbreviation__index__contains=ticker).all()
        chart_data = StockPrices.objects.filter(company_abbreviation__company_abbreviation__contains=ticker).all()

        context = super(Dashboard, self).get_context_data(**kwargs)
        context['stock_price'] = chart_data.filter(Q(company_abbreviation__company_abbreviation__contains=ticker) &
                                                   Q(date__contains=TODAY_DATE)).first()

        context['stock_price_last_week'] = chart_data.filter(Q(company_abbreviation__company_abbreviation__contains=ticker)
                                                             & Q(date__contains=LAST_WEEK_END))
        context['companies'] = queryset.filter(date__contains=TODAY_DATE)
        context['top_companies'] = queryset.filter(date__contains=TODAY_DATE).order_by('close_price')[:5]
        context['chart'] = stock_chart(chart_data)
        context['ticker'] = ticker
        return context
