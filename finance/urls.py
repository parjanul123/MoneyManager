from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Accounts
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/<int:pk>/', views.account_detail, name='account_detail'),
    path('accounts/create/', views.account_create, name='account_create'),
    path('accounts/<int:pk>/edit/', views.account_edit, name='account_edit'),
    path('accounts/<int:pk>/delete/', views.account_delete, name='account_delete'),
    
    # Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # Budgets
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    
    # Savings
    path('savings/', views.savings_list, name='savings_list'),
    path('savings/create/', views.savings_create, name='savings_create'),
    path('savings/<int:pk>/edit/', views.savings_edit, name='savings_edit'),
    path('savings/<int:pk>/delete/', views.savings_delete, name='savings_delete'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]
