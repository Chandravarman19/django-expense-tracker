from django.db import models
from django.conf import settings
from datetime import datetime

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.now)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='expenses'
    )

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
