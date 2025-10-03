from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense


# ✅ Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category']  # date auto-fills in model
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter expense title"
            }),
            'amount': forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter amount"
            }),
            'category': forms.Select(attrs={
                "class": "form-select"
            }),
        }


# ✅ Custom Registration Form with Email (for Forgot Password support)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
