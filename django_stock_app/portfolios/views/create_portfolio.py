from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolios.models.portfolio_model import Portfolio
from portfolios.forms.portfolio_create_form import CreatePortfolioForm


class CreatePortfolio(LoginRequiredMixin, CreateView):
    model = Portfolio
    form_class = CreatePortfolioForm
    template_name = 'portfolios/create_portfolio.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.portfolio_id = self.request.user.username + '_' + form.instance.name
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreatePortfolio, self).get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.filter(user__username__contains=self.request.user.username).all()
        return context
