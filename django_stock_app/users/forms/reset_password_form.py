from django.contrib.auth.forms import PasswordResetForm


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'E-mail',
             }
        )

