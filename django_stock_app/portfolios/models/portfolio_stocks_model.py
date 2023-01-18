from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from portfolios.models.portfolio_model import Portfolio
from stocks.models.stock_prices_model import StockPrices

TODAY_DATE = settings.TODAY


class PortfolioStocks(models.Model):
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE, help_text='Portfolio FK',
                                     to_field='portfolio_id')
    stock = models.CharField(max_length=10, help_text='Company Abbreviation')

    amount = models.IntegerField(help_text='Number of stocks in portfolio',
                                 validators=[MinValueValidator(Decimal('0.01'))])
    stock_price = models.DecimalField(help_text='Average stock price', max_digits=15, decimal_places=2)

    stock_buy_date = models.DateField(auto_now=True, help_text='Date of adding the stock')

    def __str__(self):
        return self.stock

    @property
    def last_stock_price(self):
        last_stock_price = StockPrices.objects.filter(models.Q(date__contains=TODAY_DATE) &
                                                      models.Q(company_abbreviation__company_abbreviation__contains=
                                                               self.stock)).first()
        return last_stock_price

    @property
    def pricing(self):
        value = round(self.last_stock_price.close_price * self.amount, 2)
        return value

    @property
    def portfolio_pricing(self):
        value = round(self.amount * self.stock_price, 2)
        return value

    @property
    def profit_loss(self):
        profit_loss = round(self.pricing - self.portfolio_pricing, 2)
        return profit_loss

    @property
    def profit_loss_percentage(self):
        percentage = round(self.profit_loss / self.portfolio_pricing, 2)
        return percentage * 100

    @property
    def portfolio_share(self):
        total_stock_amount = PortfolioStocks.objects.filter(portfolio_id=self.portfolio_id).aggregate(
            models.Sum('amount'))['amount__sum']
        stock_share = round(self.amount / total_stock_amount, 4)
        return stock_share * 100
