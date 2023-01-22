from django.test import TestCase, RequestFactory, Client
from django.shortcuts import reverse
from ..models.portfolio_model import Portfolio
from ..models.portfolio_stocks_model import PortfolioStocks
from ..views.detail_portfolio import PortfolioDetailed
from ..views.create_portfolio import CreatePortfolio
from ..views.delete_portfolio import DeletePortfolio
from ..views.buy_stocks import BuyStockPortfolio
from .. import factories
from ..forms.portfolio_create_form import CreatePortfolioForm
from stocks import factories as stock_factories


class PortfolioTest(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()
        self.user = factories.UserFactory()
        factories.PortfolioFactory.reset_sequence(0, force=True)
        factories.PortfolioFactory.create_batch(2)
        stock_factories.CompanyFactory()
        stock_factories.StockPriceFactory()
        stock_factories.LastWeekStockPriceFactory()

    def test_check_portfolio_record_in_database(self):
        """ Check if a portfolio record has been correctly created in a database."""
        portfolios = Portfolio.objects.filter(user__username='TestUser').all()
        self.assertEqual(list(portfolios.values_list('name', flat=True)), ['PortfolioTest0', 'PortfolioTest1'])
        self.assertEqual(portfolios[0].balance, 10000.00)
        self.assertEqual(portfolios[0].user.username, 'TestUser')
        self.assertEqual(portfolios[0].portfolio_id, 'TestUser_PortfolioTest0')

    def test_get_portfolio_detailed_path(self):
        """ Check if Portfolio Detailed pages is loaded."""
        request = self.request_factory.get(reverse('portfolio-detail', kwargs={'portfolio': 'PortfolioTest0'}))
        request.user = self.user
        response = PortfolioDetailed.as_view()(request, portfolio='PortfolioTest0')
        self.assertEqual(response.status_code, 200)

    def test_create_portfolio_form_the_same_name(self):
        """ Check portfolio form name validation."""
        form = CreatePortfolioForm(data={'name': 'PortfolioTest0'})
        form.username = self.user.username
        self.assertEqual(form.errors['name'], ['The portfolio already exists!'])

    def test_create_portfolio_success(self):
        """ Check if a new portfolio has been created and redirect to the portfolio page."""
        request = self.request_factory.post(reverse('portfolio-create'), data={'name': 'PortfolioTest3'})
        request.user = self.user
        response = CreatePortfolio.as_view()(request)
        response.client = Client()
        self.assertRedirects(response, expected_url=reverse('portfolio-detail', kwargs={'portfolio': 'PortfolioTest3'}),
                             target_status_code=302, fetch_redirect_response=False)

    def test_get_delete_portfolio(self):
        """Check if portfolio URI render correct template."""
        request = self.request_factory.get(reverse('portfolio-delete', kwargs={'portfolio': 'PortfolioTest1'}))
        request.user = self.user
        response = DeletePortfolio.as_view()(request, portfolio='PortfolioTest1')
        response.client = Client()
        self.assertContains(response, '<h4>Are you sure you want to delete <b><u>PortfolioTest1</u></b> ?</h4>')

    def test_post_delete_portfolio(self):
        """Check if delete portfolio has been completed correctly."""
        request = self.request_factory.post(reverse('portfolio-delete', kwargs={'portfolio': 'PortfolioTest1'}))
        request.user = self.user
        response = DeletePortfolio.as_view()(request, portfolio='PortfolioTest1')
        response.client = Client()
        self.assertRedirects(response, expected_url=reverse('home'), target_status_code=302,
                             fetch_redirect_response=False)

    def test_buy_stocks(self):
        request = self.request_factory.post(reverse('portfolio-buy', kwargs={'portfolio': 'PortfolioTest0'}),
                                            data={
                                                'stock': 'CDR',
                                                'full_stock_name': 'CDProject',
                                                'stock_price': 133.28,
                                                'amount': 1,
                                                'value': 133.28
                                            })
        request.user = self.user
        response = BuyStockPortfolio.as_view()(request, portfolio='PortfolioTest0')
        response.client = Client()
        stock = PortfolioStocks.objects.filter(portfolio_id='TestUser_PortfolioTest0').first()
        self.assertEqual(stock.amount, 1)
        self.assertEqual(float(stock.portfolio_id.balance), 10000-133.28)


