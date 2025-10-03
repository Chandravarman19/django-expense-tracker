from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.db import models


# ✅ List all expenses (with category + date filter)
@login_required
def expense_list(request):
    category_filter = request.GET.get("category")
    date_filter = request.GET.get("date")

    # Start with filtering by current user
    expenses = Expense.objects.filter(owner=request.user)

    if category_filter:
        expenses = expenses.filter(category=category_filter)

    if date_filter:
        expenses = expenses.filter(date__gte=date_filter)

    expenses = expenses.order_by('-date')

    return render(request, 'tracker/expense_list.html', {
        'expenses': expenses,
        'selected_category': category_filter,
        'selected_date': date_filter
    })


# ✅ Add a new expense
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)   # don’t save yet
            expense.owner = request.user        # ✅ assign logged-in User object
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})


# ✅ Edit an existing expense
@login_required
def edit_expense(request, obj_id):
    expense = get_object_or_404(Expense, id=obj_id, owner=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)  # ✅ bind instance
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)  # ✅ pre-fill form properly
    return render(request, 'tracker/edit_expense.html', {'form': form})


# ✅ Delete an expense
@login_required
def delete_expense(request, obj_id):
    expense = get_object_or_404(Expense, id=obj_id, owner=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect('expense_list')

    return render(request, 'tracker/delete_expense.html', {'expense': expense})


# ✅ Monthly summary (category-based aggregation)
@login_required
def monthly_summary(request):
    summary = (
        Expense.objects.filter(owner=request.user)
        .values('category')                 # group by category
        .annotate(total=models.Sum('amount'))  # ✅ use models.Sum
    )

    total_expenses = (
        Expense.objects.filter(owner=request.user)
        .aggregate(total=models.Sum('amount'))['total']
    )

    return render(request, 'tracker/monthly_summary.html', {
        'summary': summary,
        'total_expenses': total_expenses
    })


# ✅ User Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Registration successful! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


# ✅ Logout
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# ✅ Custom login (redirect admin users to /admin/)
def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            return redirect('expense_list')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})
