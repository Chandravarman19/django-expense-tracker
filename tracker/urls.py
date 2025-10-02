from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<str:obj_id>/', views.edit_expense, name='edit_expense'),   # ✅ changed to str
    path('delete/<str:obj_id>/', views.delete_expense, name='delete_expense'),  # ✅ changed to str
    path('summary/', views.monthly_summary, name='monthly_summary'),

    # ✅ Authentication
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ✅ Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
