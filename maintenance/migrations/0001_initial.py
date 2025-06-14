# Generated by Django 5.0.1 on 2025-05-07 08:14

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=50, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('active', 'Active'), ('maintenance', 'In Maintenance'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('item', models.CharField(max_length=200)),
                ('inventory', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('admin', 'Administrator'), ('technician', 'Technician')], max_length=20, unique=True)),
                ('can_add_users', models.BooleanField(default=False)),
                ('can_delete_users', models.BooleanField(default=False)),
                ('can_view_all', models.BooleanField(default=True)),
                ('can_export', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fault_date', models.DateField(blank=True, default=datetime.date(2025, 5, 7), null=True, verbose_name='Fault Date')),
                ('reported_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], max_length=20)),
                ('resolution_date', models.DateTimeField(blank=True, null=True)),
                ('resolution_notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reported_faults', to=settings.AUTH_USER_MODEL)),
                ('resolved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_faults', to=settings.AUTH_USER_MODEL)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maintenance.machine')),
            ],
        ),
        migrations.CreateModel(
            name='FaultPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='fault_photos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fault', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='maintenance.fault')),
            ],
        ),
        migrations.CreateModel(
            name='SparePartTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('add', 'Add to Inventory'), ('remove', 'Remove from Inventory')], max_length=10)),
                ('quantity', models.IntegerField()),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.machine')),
                ('spare_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='maintenance.sparepart')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.userrole')),
            ],
        ),
    ]
