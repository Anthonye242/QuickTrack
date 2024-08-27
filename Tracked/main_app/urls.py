from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication views
    path('', views.Home.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),

    # Bank Account URLs
    path('bank-accounts/', views.bank_account_index, name='bank-account-index'),
    path('bank-accounts/<int:account_id>/', views.bank_account_detail, name='bank-account-detail'),
    path('bank-accounts/create/', views.BankAccountCreate.as_view(), name='bank-account-create'),
    path('bank-accounts/<int:pk>/update/', views.BankAccountUpdate.as_view(), name='bank-account-update'),
    path('bank-accounts/<int:pk>/delete/', views.BankAccountDelete.as_view(), name='bank-account-delete'),
    
    # Transaction URLs
    path('transactions/<int:account_id>/add/', views.add_transaction, name='add-transaction'),
    path('transactions/<int:pk>/update/', views.TransactionUpdate.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.TransactionDelete.as_view(), name='transaction-delete'),
    
    # Budget URLs
    path('budgets/', views.BudgetList.as_view(), name='budget-list'),
    path('budgets/<int:pk>/', views.BudgetDetail.as_view(), name='budget-detail'),
    path('budgets/create/', views.BudgetCreate.as_view(), name='budget-create'),
    path('budgets/<int:pk>/update/', views.BudgetUpdate.as_view(), name='budget-update'),
    path('budgets/<int:pk>/delete/', views.BudgetDelete.as_view(), name='budget-delete'),

    # Expense URLs
    path('expenses/create/<int:budget_id>/', views.expense_create, name='expense-create'),
    path('expenses/<int:pk>/update/', views.ExpenseUpdate.as_view(), name='expense-update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDelete.as_view(), name='expense-delete'),
]
