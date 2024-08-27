from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import BankAccount, Transaction, Budget, Expense
from .forms import TransactionForm, BudgetForm, ExpenseForm

class Home(LoginView):
    template_name = 'home.html'

@login_required
def bank_account_index(request):
    bank_accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bank_accounts/index.html', {'bank_accounts': bank_accounts})

@login_required
def bank_account_detail(request, account_id):
    bank_account = BankAccount.objects.filter(id=account_id, user=request.user).first()
    if bank_account:
        transactions = Transaction.objects.filter(account=bank_account)
        transaction_form = TransactionForm()
        return render(request, 'bank_accounts/detail.html', {
            'bank_account': bank_account,
            'transaction_form': transaction_form,
            'transactions': transactions
        })
    return redirect('bank-account-index')

class BankAccountCreate(LoginRequiredMixin, CreateView):
    model = BankAccount
    fields = ['name', 'balance']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BankAccountUpdate(LoginRequiredMixin, UpdateView):
    model = BankAccount
    fields = ['name', 'balance']

class BankAccountDelete(LoginRequiredMixin, DeleteView):
    model = BankAccount
    success_url = '/bank-accounts/'

@login_required
def add_transaction(request, account_id):
    form = TransactionForm(request.POST)
    if form.is_valid():
        new_transaction = form.save(commit=False)
        new_transaction.account_id = account_id
        new_transaction.save()
    return redirect('bank-account-detail', account_id=account_id)

class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['description', 'amount', 'date', 'budget']

class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    
    def get_success_url(self):
        return reverse('bank-account-detail', kwargs={'account_id': self.object.account.id})

class BudgetCreate(LoginRequiredMixin, CreateView):
    model = Budget
    fields = ['name', 'amount']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetList(LoginRequiredMixin, ListView):
    model = Budget
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetDetail(LoginRequiredMixin, DetailView):
    model = Budget

class BudgetUpdate(LoginRequiredMixin, UpdateView):
    model = Budget
    fields = ['name', 'amount']

class BudgetDelete(LoginRequiredMixin, DeleteView):
    model = Budget
    success_url = '/budgets/'

@login_required
def expense_create(request, budget_id):
    budget = Budget.objects.filter(id=budget_id, user=request.user).first()
    if budget and request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.budget = budget
            new_expense.save()
            return redirect('budget-detail', pk=budget_id)
    return redirect('budget-list')

class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['description', 'amount', 'date']

class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expense
    
    def get_success_url(self):
        return reverse('budget-detail', kwargs={'pk': self.object.budget.id})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bank-account-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)