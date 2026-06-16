from django import forms
from orders.models import Order


class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select styled-select', 'id': 'payment_method_select'}),
        label=''
    )

    delivery_type = forms.ChoiceField(
        choices=Order.DELIVERY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select styled-select', 'id': 'delivery_type_select'}),
        label=''
    )
    
    bank_name = forms.CharField(max_length=100, required=False, label='Nombre del banco')
    bank_account_number = forms.CharField(max_length=50, required=False, label='Número de cuenta')

    delivery_address = forms.CharField(widget=forms.Textarea, required=False, label='Dirección completa de entrega')
    
    card_holder_name = forms.CharField(max_length=100, required=False, label='Nombre del titular de la tarjeta')
    card_number = forms.CharField(max_length=20, required=False, label='Número de tarjeta', widget=forms.TextInput(attrs={'placeholder': '**** **** **** ****'}))

    pickup_full_name = forms.CharField(max_length=200, required=False, label='Nombre completo')
    pickup_document = forms.CharField(max_length=20, required=False, label='Número de documento')
    pickup_phone = forms.CharField(max_length=20, required=False, label='Número de teléfono')
    pickup_date = forms.DateField(required=False, label='Fecha estimada', widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Ej: Banco de Bogotá'})
        self.fields['bank_account_number'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Ej: 1234567890'})

        self.fields['delivery_address'].widget.attrs.update({'class': 'form-input', 'rows': 3, 'placeholder': 'Calle, número, ciudad, etc.'})
        self.fields['card_holder_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Ej: Juan Pérez'})
        self.fields['card_number'].widget.attrs.update({'class': 'form-input', 'placeholder': '1234 5678 9012 3456'})

        # COD fields
        self.fields['pickup_full_name'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Ej: Elian Gonzalez'})
        self.fields['pickup_document'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Ej: CC 12345678'})
        self.fields['pickup_phone'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Ej: 3001234567'})
        self.fields['pickup_date'].widget.attrs.update({'class': 'form-input'})

    def clean(self):
        cleaned_data = super().clean()
        payment = cleaned_data.get('payment_method')
        delivery = cleaned_data.get('delivery_type')
        
        if payment == 'contra_entrega':
            if not cleaned_data.get('pickup_full_name'):
                self.add_error('pickup_full_name', 'Requerido para pago contra entrega')
            if not cleaned_data.get('pickup_document'):
                self.add_error('pickup_document', 'Requerido para pago contra entrega')
            if not cleaned_data.get('pickup_phone'):
                self.add_error('pickup_phone', 'Requerido para pago contra entrega')
            if not cleaned_data.get('pickup_date'):
                self.add_error('pickup_date', 'Requerido para pago contra entrega')
        
        if payment == 'transfer':
            if not cleaned_data.get('bank_name'):
                self.add_error('bank_name', 'Requerido para transferencia bancaria')
            if not cleaned_data.get('bank_account_number'):
                self.add_error('bank_account_number', 'Requerido para transferencia bancaria')
        elif payment == 'card':
            if not cleaned_data.get('card_holder_name'):
                self.add_error('card_holder_name', 'Requerido para pago con tarjeta')
            if not cleaned_data.get('card_number'):
                self.add_error('card_number', 'Requerido para pago con tarjeta')
        
        if delivery == 'delivery':
            if not cleaned_data.get('delivery_address'):
                self.add_error('delivery_address', 'Requerida para envío a domicilio')
        
        return cleaned_data

