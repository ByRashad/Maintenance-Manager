# Generated by Django 5.0.1 on 2025-05-08 12:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0002_purchaserequest_purchaseitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='fault_date',
            field=models.DateField(blank=True, default=datetime.date(2025, 5, 8), null=True, verbose_name='Fault Date'),
        ),
        migrations.AlterField(
            model_name='purchaserequest',
            name='submission_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
