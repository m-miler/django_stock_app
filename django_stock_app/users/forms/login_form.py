from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        attributes = {"class": "form-control", "placeholder": ""}

        for field_name in ["username", "password"]:
            field = self.fields[field_name]
            field.label = ""
            field.widget.attrs.update(attributes)
            field.widget.attrs["placeholder"] = field_name.capitalize()
