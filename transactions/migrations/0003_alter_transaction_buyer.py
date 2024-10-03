# Generated by Django 5.1.1 on 2024-10-03 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0001_initial'),
        ('transactions', '0002_alter_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='buyer.buyer'),
        ),
    ]