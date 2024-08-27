from django.contrib import admin
from .models import BankAccount, Transaction, Budget, Expense

admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Expense)
