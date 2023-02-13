from http import HTTPStatus

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from django.test import Client, RequestFactory, TestCase
from portfolios import factories as user_factories
from stocks import factories as stock_factories

from .views import Dashboard


class DashboardTests(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()
        self.client = Client()
        self.user = user_factories.UserFactory()
        self.company = stock_factories.CompanyFactory()
        stock_factories.StockPriceFactory.reset_sequence(1, force=True)
        self.stock_prices = stock_factories.StockPriceFactory()

    def test_home_page(self):
        """Test if home page is return when a user is correctly logged in."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_home_page_redirect(self):
        """Test if the home page redirect to the login page if a user is not logged in."""
        response = self.client.get(reverse("home"), follow=True)
        response_1 = self.client.get(
            reverse("dashboard", kwargs={"ticker": "WIG20"}), follow=True
        )
        self.assertEqual(response.redirect_chain, [("/login/", HTTPStatus.FOUND)])
        self.assertEqual(
            response_1.redirect_chain,
            [("/login/?next=/dashboard/WIG20", HTTPStatus.FOUND)],
        )

    def test_correct_template_is_render(self):
        """Test if a correct template is rendered based on ticker when user is correctly logged in."""
        ticker = "WIG20"
        ticker_1 = self.company.company_abbreviation.upper()
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard", kwargs={"ticker": ticker}))
        response_1 = self.client.get(reverse("dashboard", kwargs={"ticker": ticker_1}))
        self.assertTemplateUsed(response, "dashboard/wig.html")
        self.assertTemplateUsed(response_1, "dashboard/stock_detail.html")

    def test_anonymous_user_redirect_to_login_page(self):
        """Test if an anonymous user is redirect to the login page."""
        ticker = "WIG20"
        response = self.client.get(
            reverse("dashboard", kwargs={"ticker": ticker}), follow=True
        )
        response.user = AnonymousUser()
        self.assertTemplateUsed(response, template_name="users/login.html")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_dashboard_view_contex(self):
        """Test if all needed context data are available in rendered view."""
        ticker = self.company.company_abbreviation.upper()
        request = self.request_factory.get(
            reverse("dashboard", kwargs={"ticker": ticker})
        )
        request.user = self.user
        response = Dashboard.as_view()(request, ticker=ticker)
        self.assertIn(ticker, response.context_data["ticker"])
        self.assertIn("stock_price", response.context_data)
        self.assertIn("companies", response.context_data)
        self.assertIn("top_companies", response.context_data)
        self.assertIn("chart", response.context_data)
        self.assertIn("tweets", response.context_data)
        self.assertEqual(response.context_data["ticker"], ticker)
