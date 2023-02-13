from django.contrib.auth.forms import UserCreationForm, forms
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["username"].help_text = ""
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Username",
            }
        )

        email = forms.EmailField()
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "E-mail",
            }
        )

        self.fields["password1"].label = ""
        self.fields["password1"].help_text = ""
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Password",
            }
        )

        self.fields["password2"].label = ""
        self.fields["password2"].help_text = ""
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Password Confirmation",
            }
        )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
