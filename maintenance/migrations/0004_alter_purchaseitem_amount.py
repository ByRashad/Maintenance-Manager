# Generated by Django 5.0.1 on 2025-05-08 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0003_alter_fault_fault_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
