# Generated by Django 5.1.3 on 2025-02-12 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_item_permis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facture',
            name='user',
        ),
    ]
