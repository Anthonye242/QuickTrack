from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bank-account-detail', kwargs={'account_id': self.id})

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, related_name='budgets', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('budget-detail', kwargs={'pk': self.id})

class Transaction(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=(('income', 'Income'), ('expense', 'Expense')))

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def get_absolute_url(self):
        return reverse('transaction-detail', kwargs={'pk': self.id})

class Expense(models.Model):
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, null=True, related_name='expenses')
    budget = models.ForeignKey(Budget, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')

    def __str__(self):
        return f'{self.description} - {self.amount}'

    def get_absolute_url(self):
        return reverse('expense-detail', kwargs={'pk': self.id})
