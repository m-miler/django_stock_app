from datetime import datetime, timedelta
from django.db import models
from stocks.models.companies_model import StockCompanies

TODAY_DATE = '2022-12-29' #(datetime.date(datetime.today()) - timedelta(days=1)).strftime('%Y-%m-%d')
LAST_WEEK_END = '2022-12-22'#(datetime.date(datetime.today()) - timedelta(days=7)).strftime('%Y-%m-%d')


class StockPrices(models.Model):
    company_abbreviation = models.ForeignKey(StockCompanies,
                                             to_field='company_abbreviation',
                                             on_delete=models.CASCADE,
                                             help_text='Company Abbreviation')
    date = models.DateField(help_text='Stock Price Date')
    open_price = models.FloatField(help_text='Day Open Price')
    max_price = models.FloatField(help_text='Day Max Price')
    min_price = models.FloatField(help_text='Day Min Price')
    close_price = models.FloatField(help_text='Day Close Price')
    volume = models.BigIntegerField(help_text='Day Volume')

    def __str__(self):
        return self.company_abbreviation.company_abbreviation + '_' + self.date.strftime('%Y-%m-%d')

    def get_weekly_price(self, field_name):
        last_week_price = StockPrices.objects.filter(models.Q(date=LAST_WEEK_END) &
                                                     models.Q(company_abbreviation__company_abbreviation=
                                                              self.company_abbreviation)).first()
        if not last_week_price:
            return None

        current_value = getattr(self, field_name)
        last_week_value = getattr(last_week_price, field_name)
        weekly_change = (current_value - last_week_value) / current_value
        return Decimal(weekly_change).quantize(Decimal('0.001')) * 100

    @property
    def close_weekly_change(self):
        weekly_change = round(((self.close_price - self.last_week_price.close_price) / self.close_price), 4)
        return weekly_change * 100

    @property
    def open_weekly_change(self):
        weekly_change = round(((self.open_price - self.last_week_price.open_price) / self.open_price), 4)
        return weekly_change * 100

    @property
    def max_weekly_change(self):
        weekly_change = round(((self.max_price - self.last_week_price.max_price) / self.max_price), 4)
        return weekly_change * 100

    @property
    def min_weekly_change(self):
        weekly_change = round(((self.min_price - self.last_week_price.min_price) / self.min_price), 4)
        return weekly_change * 100

    @property
    def volume_weekly_change(self):
        return self.get_weekly_price('volume')
