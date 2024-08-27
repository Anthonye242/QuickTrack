from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('bank-accounts/', views.bank_account_index, name='bank-account-index'),
    path('bank-accounts/<int:account_id>/', views.bank_account_detail, name='bank-account-detail'),
    path('bank-accounts/create/', views.bank_account_create, name='bank-account-create'),
    path('bank-accounts/<int:account_id>/update/', views.bank_account_update, name='bank-account-update'),
    path('bank-accounts/<int:account_id>/delete/', views.bank_account_delete, name='bank-account-delete'),
    path('transactions/create/', views.transaction_create, name='transaction-create'),
    path('expenses/create/', views.expense_create, name='expense-create'),
    path('budgets/create/', views.budget_create, name='budget-create'),
    path('budgets/<int:budget_id>/update/', views.budget_update, name='budget-update'),
    path('transactions/<int:transaction_id>/update/', views.transaction_update, name='transaction-update'),
    path('transactions/<int:transaction_id>/delete/', views.transaction_delete, name='transaction-delete'),
    path('expenses/<int:expense_id>/update/', views.expense_update, name='expense-update'),
    path('expenses/<int:expense_id>/delete/', views.expense_delete, name='expense-delete'),
    path('signup/', views.signup, name='signup'),
]
