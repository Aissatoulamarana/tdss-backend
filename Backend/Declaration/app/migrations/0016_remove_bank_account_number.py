# Generated by Django 5.1.5 on 2025-01-29 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='account_number',
        ),
    ]
