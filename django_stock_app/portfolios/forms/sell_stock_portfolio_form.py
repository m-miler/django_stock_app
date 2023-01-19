from django import forms
from ..models.portfolio_stocks_model import PortfolioStocks


class SellStockPortfolioForm(forms.ModelForm):
    class Meta:
        model = PortfolioStocks
        fields = ['stock', 'full_stock_name', 'stock_price', 'amount', 'value']

    full_stock_name = forms.CharField(max_length=50, disabled=True, required=False)
    stock_price = forms.DecimalField(max_digits=15, decimal_places=2)
    value = forms.DecimalField(max_digits=15, decimal_places=2)

    def __init__(self, portfolio_id=None, *args, **kwargs):
        super(SellStockPortfolioForm, self).__init__(*args, **kwargs)
        stock_choice = PortfolioStocks.objects.filter(portfolio_id=portfolio_id).only('stock')
        self.fields['stock'] = forms.ModelChoiceField(queryset=stock_choice, to_field_name='stock')
        self.fields['stock'].label = 'Stock Ticker'
        self.fields['stock'].help_text = ''
        self.fields['stock'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'Stock Name'
             }
        )

        self.fields['full_stock_name'].label = 'Stock Full Name'
        self.fields['full_stock_name'].help_text = ''
        self.fields['full_stock_name'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': ''
             }
        )

        self.fields['stock_price'].label = 'Last Stock Price'
        self.fields['stock_price'].help_text = ''
        self.fields['stock_price'].widget.attrs.update(
            {'class': 'form-control',
             'readonly': True
             }
        )

        self.fields['amount'].label = 'Number of stocks'
        self.fields['amount'].help_text = ''
        self.fields['amount'].widget.attrs.update(
            {'class': 'form-control',
             'min': 0
             }
        )

        self.fields['value'].label = 'Value of buy stocks'
        self.fields['value'].help_text = ''
        self.fields['value'].widget.attrs.update(
            {'class': 'form-control',
             'readonly': True
             }
        )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        current_amount_of_stock = self.instance.amount
        if amount > current_amount_of_stock:
            raise forms.ValidationError('Too many stocks to sell!')
        return amount
