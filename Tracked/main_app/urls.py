from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.Home.as_view(), name='home'),
    
    # Bank account URLs
    path('bank_accounts/', views.bank_account_index, name='bank-account-index'),
    path('bank_accounts/<int:account_id>/', views.bank_account_detail, name='bank-account-detail'),
    path('bank_accounts/create/', views.bank_account_create, name='bank-account-create'),
    path('bank_accounts/<int:account_id>/update/', views.bank_account_update, name='bank-account-update'),
    path('bank_accounts/<int:account_id>/delete/', views.bank_account_delete, name='bank-account-delete'),
    
    # Transaction URLs
    path('transactions/<int:transaction_id>/update/', views.transaction_update, name='transaction-update'),
    path('transactions/<int:transaction_id>/delete/', views.transaction_delete, name='transaction-delete'),
    
    # Budget URLs
    path('budgets/', views.budget_index, name='budget-index'),
    path('budgets/create/', views.budget_create, name='budget-create'),
    
    # BudgetTransaction URLs
    path('budget_transactions/create/', views.budget_transaction_create, name='budget-transaction-create'),
    path('budget_transactions/<int:budget_transaction_id>/update/', views.budget_transaction_update, name='budget-transaction-update'),
    path('budget_transactions/<int:budget_transaction_id>/delete/', views.budget_transaction_delete, name='budget-transaction-delete'),
    
    # Expenses URLs
    path('expenses/', views.expense_index, name='expense-index'),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense-detail'),
    path('expenses/create/', views.expense_create, name='expense-create'),
    path('expenses/<int:expense_id>/update/', views.expense_update, name='expense-update'),
    path('expenses/<int:expense_id>/delete/', views.expense_delete, name='expense-delete'),
         
    # Account registration and login URLs
    path('accounts/signup/', views.signup, name='signup'),
]
