from django import forms
from portfolios.models.portfolio_stocks_model import PortfolioStocks
from portfolios.models.portfolio_model import Portfolio
from stocks.models.companies_model import StockCompanies

STOCK_CHOICES = StockCompanies.objects.only('company_abbreviation')
TODAY_DATE = '2022-12-29'


class BuyStockPortfolioForm(forms.ModelForm):
    class Meta:
        model = PortfolioStocks
        fields = ['stock', 'full_stock_name', 'stock_price', 'amount', 'value']

    stock = forms.ModelChoiceField(queryset=STOCK_CHOICES)
    full_stock_name = forms.CharField(max_length=50, disabled=True, required=False)
    stock_price = forms.DecimalField(max_digits=15, decimal_places=2)
    value = forms.DecimalField(max_digits=15, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(BuyStockPortfolioForm, self).__init__(*args, **kwargs)
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
             }
        )

        self.fields['value'].label = 'Value of buy stocks'
        self.fields['value'].help_text = ''
        self.fields['value'].widget.attrs.update(
            {'class': 'form-control',
             'readonly': True
             }
        )

    def clean_value(self):
        value = self.cleaned_data['value']
        current_balance = self.instance.portfolio_id.balance
        if value > current_balance:
            raise forms.ValidationError('The amount is higher then portfolio balance!')
        return value
