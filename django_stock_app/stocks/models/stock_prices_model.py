from django.db import models
from stocks.models.companies_model import StockCompanies


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

