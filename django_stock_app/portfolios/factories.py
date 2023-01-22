import factory
from .models.portfolio_model import Portfolio
from .models.portfolio_stocks_model import PortfolioStocks
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'TestUser'
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.pl')


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio
        django_get_or_create = ('portfolio_id',)

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'PortfolioTest{n}')
    portfolio_id = factory.LazyAttribute(lambda obj: f'{obj.user.username}_{obj.name}')

