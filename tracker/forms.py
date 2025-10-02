from django import forms

class ExpenseForm(forms.Form):
    title = forms.CharField(max_length=200)
    amount = forms.DecimalField(decimal_places=2, max_digits=10)
