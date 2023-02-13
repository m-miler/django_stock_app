from django.contrib.auth.forms import SetPasswordForm


class CustomPasswordConfirmationForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordConfirmationForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].label = ""
        self.fields["new_password1"].help_text = ""
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Password",
            }
        )

        self.fields["new_password2"].label = ""
        self.fields["new_password2"].help_text = ""
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Password Confirmation",
            }
        )
