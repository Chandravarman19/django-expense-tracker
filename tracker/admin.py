from django.contrib import admin
from .models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'owner')
    search_fields = ('title', 'amount')
    list_filter = ('date',)

admin.site.register(Expense, ExpenseAdmin)
