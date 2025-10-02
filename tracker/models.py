from mongoengine import Document, StringField, DecimalField, DateTimeField
from datetime import datetime

class Expense(Document):
    title = StringField(max_length=200, required=True)
    amount = DecimalField(precision=2, required=True)
    date = DateTimeField(default=datetime.now)
    owner = StringField(required=True)   # just store username instead of User object

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
