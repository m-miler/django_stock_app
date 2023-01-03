from django.db import models
from portfolios.models.portfolio_model import Portfolio
from stocks.models.stock_prices_model import StockPrices, TODAY_DATE


class PortfolioStocks(models.Model):
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING, help_text='Portfolio FK',
                                     to_field='portfolio_id')
    stock = models.CharField(max_length=10, help_text='Company Abbreviation', unique=True)
    stock_buy_date = models.DateField(auto_now=True, help_text='Date of adding the stock')
    amount = models.IntegerField(help_text='Number of stocks in portfolio')
    stock_price = models.FloatField(help_text='Average stock price')

    @property
    def last_stock_price(self):
        last_stock_price = StockPrices.objects.filter(models.Q(date__contains=TODAY_DATE) &
                                                    models.Q(company_abbreviation__company_abbreviation__contains=
                                                             self.stock)).first()
        return last_stock_price

    @property
    def pricing(self):
        value = self.last_stock_price.close_price * self.amount
        return value

    @property
    def profit_loss(self):
        profit_loss = self.pricing - self.amount * self.stock_price
        return profit_loss

    @property
    def profit_loss_percentage(self):
        percentage = round(self.profit_loss / (self.amount * self.stock_price), 4)
        return percentage * 100

    @property
    def portfolio_share(self):
        total_stock_amount = PortfolioStocks.objects.aggregate(models.Sum('amount'))['amount__sum']
        stock_share = self.amount / total_stock_amount
        return stock_share * 100
