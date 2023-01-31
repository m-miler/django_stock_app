import factory
from .models.stock_prices_model import StockPrices
from .models.companies_model import StockCompanies


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockCompanies
        django_get_or_create = ('company_abbreviation',)

    company_full_name = factory.Faker('pystr', min_chars=3, max_chars=10)
    company_abbreviation = factory.Faker('pystr_format', string_format='???',
                                         letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    index = 'WIG20'


class StockPriceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = StockPrices

    company_abbreviation = factory.SubFactory(CompanyFactory)
    date = factory.Sequence(lambda n: f"2023-01-{n:02}") #'2023-01-18'
    open_price = factory.Faker('pyfloat', min_value=133.00, max_value=134.00, right_digits=2)
    max_price = factory.Faker('pyfloat', min_value=133.00, max_value=134.00, right_digits=2)
    min_price = factory.Faker('pyfloat', min_value=133.00, max_value=134.00, right_digits=2)
    close_price = factory.Faker('pyfloat', min_value=133.00, max_value=134.00, right_digits=2)
    volume = factory.Faker('pyint', min_value=25000, max_value=1000000)
