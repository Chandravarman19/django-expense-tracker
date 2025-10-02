from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from bson import ObjectId   # ✅ for MongoDB IDs


# ✅ List all expenses (with category + date filter)
@login_required
def expense_list(request):
    category_filter = request.GET.get("category")
    date_filter = request.GET.get("date")

    query = {"owner": request.user.username}

    if category_filter:
        query["category"] = category_filter

    if date_filter:
        query["date__gte"] = date_filter  # from that date onward

    expenses = Expense.objects(**query).order_by('-date')

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
            expense = Expense(
                title=form.cleaned_data['title'],
                amount=form.cleaned_data['amount'],
                category=form.cleaned_data['category'],   # ✅ save category
                owner=request.user.username
            )
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})


# ✅ Edit an existing expense
@login_required
def edit_expense(request, obj_id):
    try:
        expense = Expense.objects(id=ObjectId(obj_id), owner=request.user.username).first()
    except Exception:
        expense = None

    if not expense:
        messages.error(request, "❌ Expense not found or not yours!")
        return redirect('expense_list')

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense.title = form.cleaned_data['title']
            expense.amount = form.cleaned_data['amount']
            expense.category = form.cleaned_data['category']  # ✅ update category
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(initial={
            'title': expense.title,
            'amount': expense.amount,
            'category': expense.category   # ✅ pre-fill category
        })
    return render(request, 'tracker/edit_expense.html', {'form': form})


# ✅ Delete an expense
@login_required
def delete_expense(request, obj_id):
    try:
        expense = Expense.objects(id=ObjectId(obj_id), owner=request.user.username).first()
    except Exception:
        expense = None

    if not expense:
        messages.error(request, "❌ Expense not found or not yours!")
        return redirect('expense_list')

    if request.method == "POST":
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})


# ✅ Monthly summary (category-based aggregation)
@login_required
def monthly_summary(request):
    pipeline = [
        {"$match": {"owner": request.user.username}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
    ]
    summary = list(Expense.objects.aggregate(*pipeline))

    total_expenses = sum(item["total"] for item in summary) if summary else 0

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
