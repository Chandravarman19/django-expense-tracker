from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:obj_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:obj_id>/', views.delete_expense, name='delete_expense'),
    path('summary/', views.monthly_summary, name='monthly_summary'),

    # ✅ Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login', http_method_names=['get', 'post']), name='logout'),
    


]
