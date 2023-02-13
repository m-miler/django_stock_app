from django.core.management.base import BaseCommand
from portfolios import factories
from stocks import factories as stock_factories


class Command(BaseCommand):
    """Command to populate database with some sample data."""

    help = "Populate database with sample data"

    def handle(self, *args, **kwargs):
        users = factories.UserFactory.create_batch(2)
        for user in users:
            factories.PortfolioFactory.create_batch(2, portfolio_id=user)

        companies = stock_factories.CompanyFactory.create_batch(5)
        for company in companies:
            stock_factories.StockPriceFactory.reset_sequence(1, force=True)
            stock_factories.StockPriceFactory.create_batch(
                30, company_abbreviation=company
            )

        wig = stock_factories.CompanyFactory(
            company_abbreviation="WIG20", company_full_name="WIG20"
        )
        stock_factories.StockPriceFactory.reset_sequence(1, force=True)
        stock_factories.StockPriceFactory.create_batch(30, company_abbreviation=wig)
