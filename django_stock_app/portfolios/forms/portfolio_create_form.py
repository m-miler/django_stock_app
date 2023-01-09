from django import forms
from portfolios.models.portfolio_model import Portfolio


class CreatePortfolioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreatePortfolioForm, self).__init__(*args, **kwargs)
        name = forms.CharField(label='Portfolio name', max_length=20)
        self.fields['name'].label = ''
        self.fields['name'].help_text = ''
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'Portfolio name'
             }
        )

    class Meta:
        model = Portfolio
        fields = ['name']


