from django.shortcuts import render
from portfolios.models.portfolio_model import Portfolio


def profile(request):
    portfolios = Portfolio.objects.filter(user__username=request.user.username).all()
    return render(request, 'users/profile.html', context={'portfolios': portfolios})

