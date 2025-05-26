from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.core.validators import FileExtensionValidator

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('technician', 'Technician'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    can_add_users = models.BooleanField(default=False)
    can_delete_users = models.BooleanField(default=False)
    can_view_all = models.BooleanField(default=True)
    can_export = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()

class Machine(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('inactive', 'Inactive')
    ]
    
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

class Fault(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ]
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    fault_date = models.DateField(verbose_name='Fault Date', null=True, blank=True, default=timezone.now().date())
    reported_at = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_faults')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_faults')
    resolution_date = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fault {self.id} - {self.machine.name}"

    def is_resolved(self):
        return self.status == 'resolved'

    def is_closed(self):
        return self.status == 'closed'

class FaultPhoto(models.Model):
    fault = models.ForeignKey(Fault, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='fault_photos/',
                            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.fault}"

class SparePart(models.Model):
    code = models.CharField(max_length=50, unique=True)
    item = models.CharField(max_length=200)
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.item}"

class SparePartTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('add', 'Add to Inventory'),
        ('remove', 'Remove from Inventory')
    ]
    
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.spare_part} ({self.quantity})"

class PurchaseRequest(models.Model):
    TYPE_CHOICES = [
        ('PR', 'Purchase Request'),
        ('IR', 'Item Request')
    ]
    
    INVOICE_TYPES = [
        ('invoice', 'Invoice'),
        ('general', 'General')
    ]
    
    request_number = models.CharField(max_length=50, unique=True)
    request_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    request_date = models.DateField()
    submission_date = models.DateField(null=True, blank=True)
    additional_info = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request_number} - {self.get_request_type_display()}"

    def get_item_count(self):
        return self.items.count()

    def calculate_total_price(self):
        """Calculate total price of all items in this purchase request based on received quantity."""
        total = 0
        for item in self.items.all():
            if item.price is not None and item.received_quantity is not None:
                total += item.price * item.received_quantity
        return total

class PurchaseItem(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name='items')
    invoice_type = models.CharField(max_length=20, choices=PurchaseRequest.INVOICE_TYPES)
    execution_date = models.DateField()
    product = models.CharField(max_length=200)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    received_quantity = models.IntegerField(default=0)
    submission_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.quantity} {self.unit_of_measurement}"

    def save(self, *args, **kwargs):
        # Set execution date to match request date
        self.execution_date = self.purchase_request.request_date
        
        # Update total price for purchase request based on received quantity
        total = 0
        for item in self.purchase_request.items.all():
            if item.price is not None and item.received_quantity is not None:
                total += item.price * item.received_quantity
        self.purchase_request.total_price = total
        self.purchase_request.save()
        
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    def can_add_users(self):
        return self.role and self.role.can_add_users

    def can_delete_users(self):
        return self.role and self.role.can_delete_users

    def can_view_all(self):
        return self.role and self.role.can_view_all

    def can_export(self):
        return self.role and self.role.can_export
