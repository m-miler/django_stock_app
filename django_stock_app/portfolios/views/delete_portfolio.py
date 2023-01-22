from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolios.models.portfolio_model import Portfolio


class DeletePortfolio(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolios/delete_portfolio.html'
    slug_url_kwarg = 'portfolio'
    slug_field = 'portfolio_id'
    success_url = '/'

    def get_object(self, queryset=None, *args, **kwargs):
        portfolio_id = f'{self.request.user.username}_{self.kwargs.get(self.slug_url_kwarg)}'
        obj = Portfolio.objects.filter(portfolio_id=portfolio_id).first()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DeletePortfolio, self).get_context_data(**kwargs)
        context['object'] = self.object
        context['portfolios'] = Portfolio.objects.filter(user__username=self.request.user.username).all()
        return context

