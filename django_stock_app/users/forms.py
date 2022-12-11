from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, forms
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'username',
             }
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'password'}
        )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
