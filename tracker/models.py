from django.db import models
from django.conf import settings
from datetime import datetime

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Travel", "Travel"),
        ("Bills", "Bills"),
        ("Shopping", "Shopping"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Other")  # ✅ new field
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="expenses"
    )

    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.category})"

