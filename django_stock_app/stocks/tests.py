from django.test import TestCase, override_settings
from .models.stock_prices_model import StockPrices
from .models.companies_model import StockCompanies
from . import factories


class StockModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.TODAY = '2023-01-18'
        self.LAST_WEEK_END = '2023-01-11'

        self.company = factories.CompanyFactory()
        self.current_price = factories.StockPriceFactory(date='2023-01-18',
                                                         company_abbreviation=self.company)
        self.last_price = factories.StockPriceFactory(date='2023-01-11',
                                                      company_abbreviation=self.company)

    def test_create_new_record_of_stock_price_db(self):
        """Test if a new stock price record is created correctly."""
        stock_price = StockPrices.objects.get(company_abbreviation=self.company.company_abbreviation, date=self.TODAY)
        self.assertEqual(stock_price.company_abbreviation.company_full_name, self.company.company_full_name)
        self.assertEqual(stock_price.date.strftime("%Y-%m-%d"), self.TODAY)
        self.assertTrue(isinstance(stock_price.company_abbreviation, StockCompanies))

    @override_settings(LAST_WEEK_END='2023-01-11')
    def test_stock_price_get_weekly_price(self):
        """Check stock price database property."""
        stock_price = StockPrices.objects.get(company_abbreviation=self.company.company_abbreviation, date=self.TODAY)
        close_last_week_price = stock_price.close_weekly_change
        self.assertEqual(float(stock_price.close_price), self.current_price.close_price)
        self.assertEqual(float(close_last_week_price),
                         round(((self.current_price.close_price - self.last_price.close_price) /
                                self.current_price.close_price) * 100, 2))


