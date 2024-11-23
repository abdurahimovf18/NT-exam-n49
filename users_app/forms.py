from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(), required=False)
    password_confirmation = forms.CharField(max_length=255, widget=forms.PasswordInput(), required=False)

    class Meta:
        model = UserModel
        fields = ["email", "first_name", "last_name"]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password", "")
        password_confirmation = cleaned_data.get("password_confirmation", "")

        if password and password != password_confirmation:
            raise ValidationError("Passwords should match")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        kwargs.pop("request", None)
        
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            label = key.replace("_", " ").title()
            field.widget.attrs.update(
                {
                    "placeholder": label,
                    "class": "text-light form-control form-control-lg"
                }
            )
            field.label = label


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=255, widget=forms.PasswordInput())

    class Meta:
        model = UserModel
        fields = ("email", "first_name", "last_name")

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["password"] != cleaned_data["password_confirmation"] and cleaned_data["password"]:
            raise ValidationError("Password must much ...")
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("request", None)

        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            key = key.replace("_", " ").title()

            field.widget.attrs.update(
                {
                    "placeholder": key,
                    "class": "text-light form-control form-control-lg"
                }
            )
            field.label = key


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=255,
                            widget=forms.EmailInput())
    
    password = forms.CharField(max_length=255,
                               widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        kwargs.pop("request", None)

        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            key = key.replace("_", " ").title()

            field.widget.attrs.update(
                {
                    "placeholder": key,
                    "class": "text-light form-control form-control-lg"
                }
            )
            
            field.label = key
