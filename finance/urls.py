from django.urls import path
from . import views
from . import bank_views
from . import bt_pay_views
from . import bt_pay_realtime

app_name = 'finance'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Accounts
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/<int:pk>/', views.account_detail, name='account_detail'),
    path('accounts/<int:pk>/transactions/', views.account_transactions, name='account_transactions'),
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
    
    # Bank Integration
    path('banks/', bank_views.bank_connections_list, name='bank_connections_list'),
    path('banks/create/', bank_views.bank_connection_create, name='bank_connection_create'),
    path('banks/<int:pk>/delete/', bank_views.bank_connection_delete, name='bank_connection_delete'),
    path('banks/sync/', bank_views.bank_sync_transactions, name='bank_sync_transactions'),
    path('banks/<int:pk>/sync/', bank_views.bank_sync_transactions, name='bank_sync_transactions_one'),
    path('banks/transactions/pending/', bank_views.bank_transactions_pending, name='bank_transactions_pending'),
    path('banks/<int:pk>/transactions/pending/', bank_views.bank_transactions_pending, name='bank_transaction_pending'),
    path('banks/transactions/<int:trans_pk>/accept/', bank_views.bank_transaction_accept, name='bank_transaction_accept'),
    path('banks/transactions/<int:trans_pk>/ignore/', bank_views.bank_transaction_ignore, name='bank_transaction_ignore'),
    path('banks/transactions/synced/', bank_views.bank_transactions_synced, name='bank_transactions_synced'),
    path('banks/<int:pk>/transactions/synced/', bank_views.bank_transactions_synced, name='bank_transactions_synced_one'),
    path('banks/dashboard/', bank_views.bank_dashboard, name='bank_dashboard'),
    
    # BT Pay Integration
    path('bt-pay/', bt_pay_views.bt_pay_websocket_dashboard, name='bt_pay_dashboard'),
    path('bt-pay/live/', bt_pay_views.bt_pay_live_dashboard, name='bt_pay_live_dashboard'),
    path('bt-pay/transactions/', bt_pay_views.bt_pay_transactions, name='bt_pay_transactions'),
    path('bt-pay/auto-categorize/', bt_pay_views.bt_pay_auto_categorize, name='bt_pay_auto_categorize'),
    path('bt-pay/merchant/<str:merchant_name>/', bt_pay_views.bt_pay_merchant_detail, name='bt_pay_merchant_detail'),
    path('bt-pay/analysis/', bt_pay_views.bt_pay_category_analysis, name='bt_pay_category_analysis'),
    
    # BT Pay Real-time API
    path('api/bt-pay/transactions/', bt_pay_realtime.bt_pay_live_transactions, name='api_bt_pay_transactions'),
    path('api/bt-pay/stats/', bt_pay_realtime.bt_pay_live_stats, name='api_bt_pay_stats'),
    path('api/bt-pay/pending/', bt_pay_realtime.bt_pay_live_pending, name='api_bt_pay_pending'),
    path('api/bt-pay/dashboard/', bt_pay_realtime.bt_pay_live_dashboard_data, name='api_bt_pay_dashboard'),
    path('api/bt-pay/stream/', bt_pay_realtime.stream_bt_pay_events, name='api_bt_pay_stream'),
    path('api/bt-pay/hourly/', bt_pay_realtime.bt_pay_hourly_summary, name='api_bt_pay_hourly'),
    path('api/bt-pay/categories/', bt_pay_realtime.bt_pay_category_realtime, name='api_bt_pay_categories'),
    
    # Documentation
    path('docs/bank-api-tokens/', views.bank_api_tokens_doc, name='bank_api_tokens_doc'),
]
