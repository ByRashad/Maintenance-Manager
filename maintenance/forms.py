from django import forms
from .models import SparePart, SparePartTransaction, PurchaseRequest, PurchaseItem
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
import os

def validate_excel_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise forms.ValidationError(f'Unsupported file extension. Allowed: {valid_extensions}')

class SparePartImportForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel File',
        help_text='Select an Excel file containing columns: Code, Item, Machine, Inventory',
        validators=[validate_excel_file_extension]
    )

class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['code', 'item', 'inventory']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SparePartTransactionForm(ModelForm):
    class Meta:
        model = SparePartTransaction
        fields = ['transaction_type', 'quantity', 'machine', 'transaction_date', 'notes']
        widgets = {
            'transaction_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3})
        }
        labels = {
            'transaction_type': _('Transaction Type'),
            'quantity': _('Quantity'),
            'machine': _('Machine (for removal only)'),
            'transaction_date': _('Transaction Date'),
            'notes': _('Notes')
        }
        help_texts = {
            'machine': _('Required only when removing from inventory')
        }

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        
        if transaction_type == 'remove' and not cleaned_data.get('machine'):
            self.add_error('machine', _('Machine is required when removing from inventory'))
            
        if quantity and quantity <= 0:
            self.add_error('quantity', _('Quantity must be greater than zero'))

        return cleaned_data

class TransactionFilterForm(forms.Form):
    start_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Start Date'
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='End Date'
    )
    spare_part = forms.ModelChoiceField(
        queryset=SparePart.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Spare Part'
    )
    export_format = forms.ChoiceField(
        required=False,
        choices=[('excel', 'Excel'), ('pdf', 'PDF')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Export Format'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spare_part'].queryset = SparePart.objects.all()
        self.fields['spare_part'].label_from_instance = lambda obj: f"{obj.code} - {obj.item}"

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['request_number', 'request_type', 'request_date', 'additional_info']
        widgets = {
            'request_number': forms.TextInput(attrs={'class': 'form-control'}),
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'request_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_of_measurement', 'notes']
        widgets = {
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PurchaseItemEditForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['invoice_type', 'received_quantity', 'price', 'submission_date', 'notes']
        widgets = {
            'invoice_type': forms.Select(attrs={'class': 'form-control'}),
            'received_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'submission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'product': 'Item',
            'unit_of_measurement': 'UOM'
        }

class PurchaseFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='From Date'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='To Date'
    )

class SparePartsFilterForm(forms.Form):
    spare_part = forms.ModelChoiceField(
        queryset=SparePart.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Spare Part'
    )
    start_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Start Date'
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='End Date'
    )
    export_format = forms.ChoiceField(
        required=False,
        choices=[('excel', 'Excel'), ('pdf', 'PDF')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Export Format'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spare_part'].queryset = SparePart.objects.all()
        self.fields['spare_part'].label_from_instance = lambda obj: f"{obj.code} - {obj.item}"
