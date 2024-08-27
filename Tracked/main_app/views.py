from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.views import LoginView
from .models import BankAccount, Transaction, Budget, Expense, BudgetTransaction
from .forms import BankAccountForm, TransactionForm, BudgetForm, ExpenseForm, BudgetTransactionForm

class Home(LoginView):
    template_name = 'home.html'

@login_required
def bank_account_index(request):
    bank_accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bank_accounts/index.html', {'bank_accounts': bank_accounts})

@login_required
def bank_account_detail(request, account_id):
    bank_account = BankAccount.objects.filter(id=account_id, user=request.user).first()
    transactions = Transaction.objects.filter(account=bank_account) if bank_account else []
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid() and bank_account:
            new_transaction = transaction_form.save(commit=False)
            new_transaction.account = bank_account
            new_transaction.save()
            return redirect('bank-account-detail', account_id=account_id)
    else:
        transaction_form = TransactionForm()
    return render(request, 'bank_accounts/detail.html', {
        'bank_account': bank_account,
        'transaction_form': transaction_form,
        'transactions': transactions
    })

@login_required
def bank_account_create(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('bank-account-index')
    else:
        form = BankAccountForm()
    return render(request, 'bank_accounts/create.html', {'form': form})

@login_required
def bank_account_update(request, account_id):
    bank_account = BankAccount.objects.filter(id=account_id, user=request.user).first()
    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=bank_account)
        if form.is_valid() and bank_account:
            form.save()
            return redirect('bank-account-detail', account_id=account_id)
    else:
        form = BankAccountForm(instance=bank_account) if bank_account else BankAccountForm()
    return render(request, 'bank_accounts/update.html', {'form': form, 'bank_account': bank_account})

@login_required
def bank_account_delete(request, account_id):
    bank_account = BankAccount.objects.filter(id=account_id, user=request.user).first()
    if request.method == 'POST' and bank_account:
        bank_account.delete()
        return redirect('bank-account-index')
    return render(request, 'bank_accounts/delete.html', {'bank_account': bank_account})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.account_id = request.POST.get('account')
            new_transaction.save()
            return redirect('bank-account-detail', account_id=new_transaction.account.id)
    else:
        form = TransactionForm()
    return render(request, 'transactions/create.html', {'form': form})

@login_required
def transaction_update(request, transaction_id):
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid() and transaction:
            form.save()
            return redirect('bank-account-detail', account_id=transaction.account.id)
    else:
        form = TransactionForm(instance=transaction) if transaction else TransactionForm()
    return render(request, 'transactions/update.html', {'form': form, 'transaction': transaction})

@login_required
def transaction_delete(request, transaction_id):
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if request.method == 'POST' and transaction:
        account_id = transaction.account.id
        transaction.delete()
        return redirect('bank-account-detail', account_id=account_id)
    return render(request, 'transactions/delete.html', {'transaction': transaction})

@login_required
def budget_create(request):
    account_id = request.GET.get('account_id')
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            new_budget = form.save(commit=False)
            new_budget.account_id = account_id
            new_budget.save()
            return redirect('bank-account-detail', account_id=account_id)
    else:
        form = BudgetForm()
    return render(request, 'budgets/create.html', {'form': form})


@login_required
def budget_index(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budgets/index.html', {'budgets': budgets})

@login_required
def budget_update(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('bank-account-detail', account_id=budget.account.id)
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'budgets/update.html', {'form': form})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()

    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

@login_required
def budget_transaction_create(request):
    if request.method == 'POST':
        form = BudgetTransactionForm(request.POST)
        if form.is_valid():
            budget_transaction = form.save()
            return redirect('budget-index')
    else:
        form = BudgetTransactionForm()
    return render(request, 'budget_transactions/create.html', {'form': form})

@login_required
def budget_transaction_update(request, budget_transaction_id):
    budget_transaction = BudgetTransaction.objects.filter(id=budget_transaction_id).first()
    if request.method == 'POST':
        form = BudgetTransactionForm(request.POST, instance=budget_transaction)
        if form.is_valid() and budget_transaction:
            form.save()
            return redirect('budget-index')
    else:
        form = BudgetTransactionForm(instance=budget_transaction) if budget_transaction else BudgetTransactionForm()
    return render(request, 'budget_transactions/update.html', {'form': form, 'budget_transaction': budget_transaction})

@login_required
def budget_transaction_delete(request, budget_transaction_id):
    budget_transaction = BudgetTransaction.objects.filter(id=budget_transaction_id).first()
    if request.method == 'POST' and budget_transaction:
        budget_transaction.delete()
        return redirect('budget-index')
    return render(request, 'budget_transactions/delete.html', {'budget_transaction': budget_transaction})

@login_required
def expense_index(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/index.html', {'expenses': expenses})

@login_required
def expense_detail(request, expense_id):
    expense = Expense.objects.filter(id=expense_id, user=request.user).first()
    return render(request, 'expenses/detail.html', {'expense': expense})

@login_required
def expense_create(request):
    account_id = request.GET.get('account_id')
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.account_id = account_id
            new_expense.user = request.user 
            new_expense.save()
            return redirect('bank-account-detail', account_id=account_id)
    else:
        form = ExpenseForm()
    return render(request, 'expenses/create.html', {'form': form})


@login_required
def expense_update(request, expense_id):
    expense = Expense.objects.filter(id=expense_id, user=request.user).first()
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid() and expense:
            form.save()
            return redirect('expense-detail', expense_id=expense.id)
    else:
        form = ExpenseForm(instance=expense) if expense else ExpenseForm()
    return render(request, 'expenses/update.html', {'form': form, 'expense': expense})

@login_required
def expense_delete(request, expense_id):
    expense = Expense.objects.filter(id=expense_id, user=request.user).first()
    if request.method == 'POST' and expense:
        expense.delete()
        return redirect('expense-index')
    return render(request, 'expenses/delete.html', {'expense': expense})
