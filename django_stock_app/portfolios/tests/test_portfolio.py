from http import HTTPStatus

from django.shortcuts import reverse
from django.test import Client, RequestFactory, TestCase, override_settings
from stocks import factories as stock_factories

from .. import factories
from ..forms.buy_stock_portfolio_form import BuyStockPortfolioForm
from ..forms.portfolio_create_form import CreatePortfolioForm
from ..forms.sell_stock_portfolio_form import SellStockPortfolioForm
from ..models.portfolio_model import Portfolio
from ..models.portfolio_stocks_model import PortfolioStocks
from ..views.buy_stocks import BuyStockPortfolio
from ..views.create_portfolio import CreatePortfolio
from ..views.delete_portfolio import DeletePortfolio
from ..views.detail_portfolio import PortfolioDetailed


class PortfolioTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.request_factory = RequestFactory()
        factories.UserFactory.reset_sequence(0, force=True)
        self.user = factories.UserFactory()
        self.company = stock_factories.CompanyFactory()
        factories.PortfolioFactory.reset_sequence(0, force=True)
        self.portfolios = factories.PortfolioFactory.create_batch(2, user=self.user)
        self.portfolio_stock = factories.PortfolioStockFactory(
            portfolio_id=self.portfolios[1], stock=self.company.company_abbreviation
        )
        stock_factories.StockPriceFactory.reset_sequence(1, force=True)
        self.current_price = stock_factories.StockPriceFactory(
            company_abbreviation=self.company
        )

    def test_check_portfolio_record_in_database(self):
        """Test if a portfolio record has been correctly created in a database."""
        portfolios = Portfolio.objects.filter(user__username="TestUser0").all()
        self.assertEqual(
            list(portfolios.values_list("name", flat=True)),
            ["PortfolioTest0", "PortfolioTest1"],
        )
        self.assertEqual(portfolios[0].balance, 10000.00)
        self.assertEqual(portfolios[0].user.username, "TestUser0")
        self.assertEqual(portfolios[0].portfolio_id, "TestUser0_PortfolioTest0")

    def test_get_portfolio_detailed_path(self):
        """Test if a portfolio detailed page is loaded."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("portfolio-detail", kwargs={"portfolio": "PortfolioTest0"})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name="portfolios/portfolio.html")

    def test_create_portfolio_form_the_same_name(self):
        """Test a portfolio form name validation."""
        form = CreatePortfolioForm(data={"name": "PortfolioTest0"})
        form.username = self.user.username
        self.assertEqual(form.errors["name"], ["The portfolio already exists!"])

    def test_create_portfolio_success(self):
        """Test if a new portfolio has been created and redirect to the portfolio page."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("portfolio-create"), data={"name": "PortfolioTest3"}
        )
        self.assertRedirects(
            response,
            expected_url=reverse(
                "portfolio-detail", kwargs={"portfolio": "PortfolioTest3"}
            ),
            target_status_code=HTTPStatus.FOUND,
            fetch_redirect_response=False,
        )

    def test_get_delete_portfolio(self):
        """Test if a portfolio URI render correct template."""
        request = self.request_factory.get(
            reverse("portfolio-delete", kwargs={"portfolio": "PortfolioTest1"})
        )
        request.user = self.user
        response = DeletePortfolio.as_view()(request, portfolio="PortfolioTest1")
        self.assertContains(
            response,
            "<h4>Are you sure you want to delete <b><u>PortfolioTest1</u></b> ?</h4>",
        )

    def test_post_delete_portfolio(self):
        """Test if a portfolio deletion has been completed correctly."""
        request = self.request_factory.post(
            reverse("portfolio-delete", kwargs={"portfolio": "PortfolioTest1"})
        )
        request.user = self.user
        response = DeletePortfolio.as_view()(request, portfolio="PortfolioTest1")
        self.assertRedirects(
            response,
            expected_url=reverse("home"),
            target_status_code=HTTPStatus.FOUND,
            fetch_redirect_response=False,
        )

    def test_buy_stocks(self):
        """Test a buy stock has been completed correctly."""
        self.client.force_login(self.user)
        for num in range(2):
            request = self.client.post(
                reverse("portfolio-buy", kwargs={"portfolio": "PortfolioTest0"}),
                data={
                    "stock": self.company.company_abbreviation,
                    "full_stock_name": self.company.company_full_name,
                    "stock_price": self.current_price.close_price,
                    "amount": 2,
                    "value": 2 * self.current_price.close_price,
                },
            )
            request.user = self.user

        stock = PortfolioStocks.objects.filter(
            portfolio_id="TestUser0_PortfolioTest0"
        ).first()
        self.assertEqual(stock.amount, 4)
        self.assertEqual(
            float(stock.portfolio_id.balance),
            10000 - 4 * self.current_price.close_price,
        )

    def test_buy_stock_view(self):
        """Test the buy stock view."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("portfolio-buy", kwargs={"portfolio": "PortfolioTest0"})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response, template_name="portfolios/buy_stock_portfolio.html"
        )
        self.assertIn("form", response.context_data)
        self.assertIn("portfolios", response.context_data)

    def test_buy_stocks_form_validators(self):
        """Test if a buying stock form return correct value validation error."""
        form = BuyStockPortfolioForm(
            data={
                "stock": self.company.company_abbreviation,
                "full_stock_name": self.company.company_full_name,
                "stock_price": self.current_price.close_price,
                "amount": 1000,
                "value": self.current_price.close_price * 1000,
            }
        )
        form.portfolio_id = "TestUser0_PortfolioTest0"
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"], ["The amount is higher then portfolio balance!"]
        )

    def test_sell_stock(self):
        """Test if stock sales are correct."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("portfolio-sell", kwargs={"portfolio": "PortfolioTest1"}),
            data={
                "stock": self.company.company_abbreviation,
                "full_stock_name": self.company.company_full_name,
                "stock_price": self.current_price.close_price,
                "amount": 2,
                "value": 2 * self.current_price.close_price,
            },
        )

        stocks = PortfolioStocks.objects.filter(
            portfolio_id="TestUser0_PortfolioTest1"
        ).first()
        self.assertEqual(stocks.amount, self.portfolio_stock.amount - 2)
        self.assertEqual(stocks.portfolio_id.balance, 10000 + 2 * stocks.stock_price)

    def test_sell_stock_form_validation(self):
        """Test if stock sales form return correct validation error."""
        form = SellStockPortfolioForm(
            data={
                "stock": self.company.company_abbreviation,
                "full_stock_name": self.company.company_full_name,
                "stock_price": self.current_price.close_price,
                "amount": 20,
                "value": self.current_price.close_price,
            }
        )
        form.portfolio_id = "TestUser0_PortfolioTest1"

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["amount"], ["Too many stocks to sell!"])
