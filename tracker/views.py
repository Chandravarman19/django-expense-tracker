from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.http import HttpResponse
from django.db.models import Sum

# List all expenses
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})

# Add a new expense
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')  # go back to list after saving
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

# ✅ Edit an existing expense
def edit_expense(request, obj_id):
    expense = get_object_or_404(Expense, id=obj_id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form})

# Delete placeholder (we’ll update next)
# Delete an expense
def delete_expense(request, obj_id):
    expense = get_object_or_404(Expense, id=obj_id)
    if request.method == "POST":
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})




# ... your other functions ...

def monthly_summary(request):
    # Group expenses by category and sum amounts
    summary = Expense.objects.values('title').annotate(total=Sum('amount'))

    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total']

    return render(request, 'tracker/monthly_summary.html', {
        'summary': summary,
        'total_expenses': total_expenses
    })

