from django.test import TestCase, override_settings
from .models.stock_prices_model import StockPrices
from .models.companies_model import StockCompanies
from . import factories


class StockModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.TODAY = '2023-01-18'
        self.LAST_WEEK_END = '2023-01-11'

        factories.CompanyFactory()
        factories.StockPriceFactory()
        factories.LastWeekStockPriceFactory()

    def test_create_new_record_of_stock_price_db(self):
        """Check if a new stock price record is created correctly."""
        stock_price = StockPrices.objects.get(company_abbreviation='CDR', date=self.TODAY)
        self.assertEqual(stock_price.company_abbreviation.company_full_name, 'CDProject')
        self.assertEqual(stock_price.date.strftime("%Y-%m-%d"), self.TODAY)
        self.assertTrue(isinstance(stock_price.company_abbreviation, StockCompanies))

    @override_settings(LAST_WEEK_END='2023-01-11')
    def test_stock_price_get_weekly_price(self):
        """Check stock price database property."""
        stock_price = StockPrices.objects.get(company_abbreviation='CDR', date=self.TODAY)
        close_last_week_price = stock_price.close_weekly_change
        self.assertEqual(float(stock_price.close_price), 133.28)
        self.assertEqual(float(close_last_week_price), round((133.28 - 135.76) / 133.28 * 100, 2))


