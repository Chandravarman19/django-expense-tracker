from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages


# ✅ List all expenses (only for logged-in user)
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})


# ✅ Add a new expense
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.owner = request.user  # link expense to logged-in user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})


# ✅ Edit an existing expense (only if user owns it)
@login_required
def edit_expense(request, obj_id):
    expense = get_object_or_404(Expense, id=obj_id, owner=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form})


# ✅ Delete an expense (only if user owns it)
@login_required
def delete_expense(request, obj_id):
    expense = get_object_or_404(Expense, id=obj_id, owner=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})


# ✅ Monthly summary (only user’s data)
@login_required
def monthly_summary(request):
    summary = (
        Expense.objects.filter(owner=request.user)
        .values('title')
        .annotate(total=Sum('amount'))
    )
    total_expenses = (
        Expense.objects.filter(owner=request.user)
        .aggregate(total=Sum('amount'))['total']
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
            user = form.save()
            login(request, user)

            # ✅ If superuser → redirect to admin dashboard
            if user.is_superuser:
                messages.success(request, "Welcome Admin! Redirecting to Dashboard.")
                return redirect('/admin/')

            # ✅ Else normal user
            messages.success(request, "✅ Registration successful! You are now logged in.")
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


# ✅ Logout
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# ✅ Custom Login
def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ✅ If superuser → go to Django Admin
            if user.is_superuser:
                return redirect('/admin/')

            # ✅ Else → go to app
            return redirect('expense_list')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})
