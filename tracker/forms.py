from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category']  # ✅ no 'date'
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
