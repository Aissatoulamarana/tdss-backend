# Generated by Django 5.1.3 on 2025-02-19 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_rename_nationalite_item_telephone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='declaration',
            name='create_date',
        ),
    ]
