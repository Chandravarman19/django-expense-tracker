from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:obj_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:obj_id>/', views.delete_expense, name='delete_expense'),
    path('summary/', views.monthly_summary, name='monthly_summary'),
]
