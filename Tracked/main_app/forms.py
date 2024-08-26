from django import forms
from .models import BankAccount, Transaction, Budget, BudgetTransaction, Expense

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_type', 'amount', 'description', 'date']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['budget_name', 'amount', 'start_date', 'end_date']

class BudgetTransactionForm(forms.ModelForm):
    class Meta:
        model = BudgetTransaction
        fields = ['budget', 'transaction', 'amount']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }