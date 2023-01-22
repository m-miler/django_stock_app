import factory
from .models.stock_prices_model import StockPrices
from .models.companies_model import StockCompanies


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockCompanies
        django_get_or_create = ('company_abbreviation',)

    company_full_name = 'CDProject'
    company_abbreviation = 'CDR'
    index = 'WIG20'


class StockPriceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = StockPrices

    company_abbreviation = factory.SubFactory(CompanyFactory)
    date = '2023-01-18'
    open_price = 129.22
    max_price = 134.8
    min_price = 129.22
    close_price = 133.28
    volume = 327117


class LastWeekStockPriceFactory(StockPriceFactory):
    date = '2023-01-11'
    open_price = 138.34
    max_price = 139.38
    min_price = 134.3
    close_price = 135.76
    volume = 460254