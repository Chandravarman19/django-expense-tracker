from django.db import models
from django.conf import settings
from django.utils import timezone   # better than datetime.now

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
    date = models.DateField(default=timezone.now)  # ✅ auto set today if not provided
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Other")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.category})"
