from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.views import LoginView
from .models import BankAccount, Transaction, Budget, Expense
from .forms import BankAccountForm, TransactionForm, BudgetForm, ExpenseForm

class Home(LoginView):
    template_name = 'home.html'

@login_required
def bank_account_index(request):
    bank_accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bank_accounts/index.html', {'bank_accounts': bank_accounts})

def bank_account_detail(request, account_id):
    bank_account = BankAccount.objects.filter(id=account_id, user=request.user).first()
    if bank_account:
        transactions = Transaction.objects.filter(account=bank_account)
        budgets = Budget.objects.filter(bank_account=bank_account)
        expenses = Expense.objects.filter(budget__bank_account=bank_account).order_by('date')
        
        if request.method == 'POST':
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                new_transaction = transaction_form.save(commit=False)
                new_transaction.account = bank_account
                new_transaction.save()
                return redirect('bank-account-detail', account_id=account_id)
        else:
            transaction_form = TransactionForm()

        return render(request, 'bank_accounts/detail.html', {
            'bank_account': bank_account,
            'transaction_form': transaction_form,
            'transactions': transactions,
            'budgets': budgets,
            'expenses': expenses,
        })
    return redirect('bank-account-index')

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
    if bank_account:
        if request.method == 'POST':
            form = BankAccountForm(request.POST, instance=bank_account)
            if form.is_valid():
                form.save()
                return redirect('bank-account-detail', account_id=account_id)
        else:
            form = BankAccountForm(instance=bank_account)
        return render(request, 'bank_accounts/update.html', {'form': form, 'bank_account': bank_account})
    return redirect('bank-account-index')

@login_required
def bank_account_delete(request, account_id):
    bank_account = BankAccount.objects.filter(id=account_id, user=request.user).first()
    if bank_account:
        if request.method == 'POST':
            bank_account.delete()
            return redirect('bank-account-index')
        return render(request, 'bank_accounts/delete.html', {'bank_account': bank_account})
    return redirect('bank-account-index')

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
    if transaction:
        if request.method == 'POST':
            form = TransactionForm(request.POST, instance=transaction)
            if form.is_valid():
                form.save()
                return redirect('bank-account-detail', account_id=transaction.account.id)
        else:
            form = TransactionForm(instance=transaction)
        return render(request, 'transactions/update.html', {'form': form, 'transaction': transaction})
    return redirect('bank-account-detail', account_id=transaction.account.id)

@login_required
def transaction_delete(request, transaction_id):
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if transaction:
        if request.method == 'POST':
            account_id = transaction.account.id
            transaction.delete()
            return redirect('bank-account-detail', account_id=account_id)
        return render(request, 'transactions/delete.html', {'transaction': transaction})
    return redirect('bank-account-detail', account_id=transaction.account.id)

@login_required
def budget_create(request):
    account_id = request.GET.get('account_id')
    bank_account = BankAccount.objects.filter(id=account_id, user=request.user).first()
    if bank_account:
        if request.method == 'POST':
            form = BudgetForm(request.POST)
            if form.is_valid():
                new_budget = form.save(commit=False)
                new_budget.bank_account = bank_account
                new_budget.user = request.user
                new_budget.save()
                return redirect('bank-account-detail', account_id=account_id)
        else:
            form = BudgetForm()
        return render(request, 'budgets/create.html', {'form': form})
    return redirect('bank-account-index')

@login_required
def budget_index(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budgets/index.html', {'budgets': budgets})

@login_required
def budget_detail(request, budget_id):
    budget = Budget.objects.filter(id=budget_id, user=request.user).first()
    if budget:
        return render(request, 'budgets/detail.html', {'budget': budget})
    return redirect('budget-index')

@login_required
def budget_update(request, budget_id):
    budget = Budget.objects.filter(id=budget_id, user=request.user).first()
    if budget:
        if request.method == 'POST':
            form = BudgetForm(request.POST, instance=budget)
            if form.is_valid():
                form.save()
                return redirect('bank-account-detail', account_id=budget.bank_account.id)
        else:
            form = BudgetForm(instance=budget)
        return render(request, 'budgets/update.html', {
            'form': form,
            'account_id': budget.bank_account.id  
        })
    return redirect('budget-index')

@login_required
def budget_delete(request, budget_id):
    budget = Budget.objects.filter(id=budget_id, user=request.user).first()
    if budget:
        if request.method == 'POST':
            bank_account_id = budget.bank_account.id
            budget.delete()
            return redirect('bank-account-detail', account_id=bank_account_id)
        return render(request, 'budgets/delete.html', {'budget': budget})
    return redirect('budget-index')

@login_required
def expense_index(request):
    expenses = Expense.objects.filter(budget__bank_account__user=request.user).order_by('-date')
    return render(request, 'expenses/index.html', {'expenses': expenses})

@login_required
def expense_detail(request, expense_id):
    expense = Expense.objects.filter(id=expense_id, budget__bank_account__user=request.user).first()
    if expense:
        return render(request, 'expenses/detail.html', {'expense': expense})
    else:
        return redirect('expense-index')

@login_required
def expense_create(request):
    account_id = request.GET.get('account_id')
    budget_id = request.GET.get('budget_id')
    
    if not account_id:
        return redirect('bank-account-index')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.budget = Budget.objects.filter(id=budget_id, bank_account_id=account_id, user=request.user).first()
            print(new_expense)
            # new_expense.save()
            # messages.success(request, "Expense created successfully.")
            # return redirect('bank-account-detail', account_id=account_id)
    else:
        form = ExpenseForm()
        if budget_id:
            form.fields['budget'].initial = budget_id

    context = {
        'form': form, 
        'account_id': account_id, 
        'budget_id': budget_id
    }
    return render(request, 'expenses/create.html', context)


@login_required
def expense_update(request, expense_id):
    expense = Expense.objects.filter(id=expense_id, user=request.user).first()
    if expense:
        if request.method == 'POST':
            form = ExpenseForm(request.POST, instance=expense)
            if form.is_valid():
                form.save()
                return redirect('expense-detail', expense_id=expense.id)
        else:
            form = ExpenseForm(instance=expense)
        return render(request, 'expenses/update.html', {'form': form, 'expense': expense})
    return redirect('expense-detail', expense_id=expense_id)

@login_required
def expense_delete(request, expense_id):
    expense = Expense.objects.filter(id=expense_id, user=request.user).first()
    if expense:
        if request.method == 'POST':
            expense.delete()
            return redirect('expense-index')
        return render(request, 'expenses/delete.html', {'expense': expense})
    return redirect('expense-index')

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
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})
