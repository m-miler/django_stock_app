from django import forms
from portfolios.models.portfolio_model import Portfolio


class CreatePortfolioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop('username', None)
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

    def clean_name(self):
        portfolio_id = self.username + '_' + self.cleaned_data['name']
        if Portfolio.objects.filter(portfolio_id=portfolio_id).count() > 0:
            raise forms.ValidationError('The portfolio already exists!')
        return self.cleaned_data['name']


