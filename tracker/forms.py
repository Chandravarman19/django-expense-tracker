from django import forms

class ExpenseForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        label="Title",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter expense title"})
    )
    amount = forms.DecimalField(
        decimal_places=2,
        max_digits=10,
        label="Amount",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter amount"})
    )
    category = forms.ChoiceField(
        choices=[
            ("Food", "Food"),
            ("Travel", "Travel"),
            ("Bills", "Bills"),
            ("Shopping", "Shopping"),
            ("Other", "Other")
        ],
        label="Category",
        widget=forms.Select(attrs={"class": "form-select"})
    )
