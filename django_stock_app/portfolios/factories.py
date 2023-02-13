import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from users.models import Profile

from .models.portfolio_model import Portfolio
from .models.portfolio_stocks_model import PortfolioStocks


@factory.django.mute_signals(post_save)
class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory("portfolios.factories.UserFactory", profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"TestUser{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.pl")
    password = factory.PostGenerationMethodCall("set_password", "test1234")
    profile = factory.RelatedFactory(UserProfileFactory, factory_related_name="user")


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio
        django_get_or_create = ("portfolio_id",)

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"PortfolioTest{n}")
    portfolio_id = factory.LazyAttribute(lambda obj: f"{obj.user.username}_{obj.name}")


class PortfolioStockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PortfolioStocks
        django_get_or_create = ("stock",)

    portfolio_id = factory.SubFactory(PortfolioFactory)
    stock = ""
    amount = factory.Faker("pyint", min_value=5, max_value=10)
    stock_price = factory.Faker(
        "pyfloat", min_value=133.00, max_value=134.00, right_digits=2
    )
