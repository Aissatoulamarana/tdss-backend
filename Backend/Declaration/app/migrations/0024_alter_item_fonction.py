# Generated by Django 5.1.3 on 2025-02-12 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_item_empreinte_item_recto_item_signature_item_verso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='fonction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app.fonction'),
        ),
    ]
