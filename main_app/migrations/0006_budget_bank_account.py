# Generated by Django 5.1 on 2024-08-27 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_remove_expense_user_expense_budget_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='bank_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='main_app.bankaccount'),
        ),
    ]
