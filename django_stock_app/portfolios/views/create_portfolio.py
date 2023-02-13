from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from ..forms.portfolio_create_form import CreatePortfolioForm
from ..models.portfolio_model import Portfolio


class CreatePortfolio(LoginRequiredMixin, CreateView):
    model = Portfolio
    form_class = CreatePortfolioForm
    template_name = "portfolios/create_portfolio.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.portfolio_id = (
            f"{self.request.user.username}_{form.instance.name}"
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreatePortfolio, self).get_form_kwargs()
        kwargs["username"] = self.request.user.username
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreatePortfolio, self).get_context_data(**kwargs)
        context["portfolios"] = self.model.objects.filter(
            user__username=self.request.user.username
        ).all()
        return context
