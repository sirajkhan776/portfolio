from django import forms
from django.contrib.auth.models import User
from .models import UserPreference


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Create a password"}),
        strip=False,
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Confirm password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"autofocus": True, "placeholder": "Choose a username"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = [
            "theme",
            "reduce_motion",
            "accent",
            "density",
            "default_section",
            "show_email",
            "show_phone",
        ]
        widgets = {
            "theme": forms.RadioSelect,
            "reduce_motion": forms.CheckboxInput,
            "accent": forms.RadioSelect,
            "density": forms.RadioSelect,
            "default_section": forms.Select,
            "show_email": forms.CheckboxInput,
            "show_phone": forms.CheckboxInput,
        }
