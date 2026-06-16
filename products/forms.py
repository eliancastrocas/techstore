from django import forms
from .models import Product, FormRequest, Service


class ProductForm(forms.ModelForm):
    # Checkbox: si no viene en POST, Django lo interpreta como False.
    is_damaged = forms.BooleanField(required=False, initial=False, label="¿Producto dañado?")

    # Garantía: para permitir edición parcial, que no falle si no se envía.
    warranty_months = forms.ChoiceField(required=False)
    warranty_type = forms.ChoiceField(required=False)
    warranty_details = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"class": "form-control", "rows": 3, "placeholder": "Detalles de la garantía..."}
    ))

    class Meta:
        model = Product
        exclude = ["seller"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del producto"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción del producto",
                    "rows": 4,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Precio",
                    "min": "0",
                }
            ),
            "image_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://ejemplo.com/imagen.jpg",
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cantidad en stock",
                    "min": "0",
                }
            ),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_service": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_damaged": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "warranty_months": forms.Select(attrs={"class": "form-control"}),
            "warranty_type": forms.Select(attrs={"class": "form-control"}),
            "warranty_details": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Detalles de la garantía..."}),
        }


class FormRequestForm(forms.ModelForm):
    device_model = forms.CharField(
        max_length=200,
        label="Modelo del dispositivo",
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'Ej: iPhone 14 Pro, Samsung Galaxy S23, MacBook Air M2'
        }),
        required=True
    )
    issue_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control-custom',
            'rows': 5,
            'placeholder': 'Describa el problema detalladamente. ¿Cuándo empezó? ¿Qué síntomas presenta? ¿Ya intentó algo?'
        }),
        label="Descripción del problema",
        required=True
    )
    images = forms.FileField(
        label="Fotos del dispositivo (opcional)",
        widget=forms.FileInput(attrs={'class': 'form-control-custom'}),
        required=False,
        help_text="Puede subir múltiples fotos (máx 5MB total)"
    )

    customer_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'Juan Pérez'
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': '+57 312 565 6485'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'cliente@ejemplo.com'
        })
    )

    service_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    issue_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    service_option = forms.CharField(widget=forms.HiddenInput(), required=False)
    priority = forms.CharField(widget=forms.HiddenInput(), initial='normal', required=False)
    description = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = FormRequest
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device_model'].label = "📱 Modelo del dispositivo"
        self.fields['issue_description'].label = "🔍 Descripción detallada del problema"
        self.fields['images'].label = "📸 Fotos del problema (opcional)"
        self.fields['customer_name'].label = "👤 Nombre completo"
        self.fields['phone'].label = "📞 Teléfono de contacto"
        self.fields['email'].label = "✉️ Email"

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Map custom fields to model fields
        instance.customer_name = self.cleaned_data['customer_name']
        instance.phone = self.cleaned_data['phone']
        instance.email = self.cleaned_data['email']
        instance.device = self.cleaned_data['device_model']
        instance.description = self.cleaned_data['issue_description']
        
        # Handle files
        if self.files.getlist('images'):
            instance.files = [f.name for f in self.files.getlist('images')]
        
        if commit:
            instance.save()
        return instance


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ["seller"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del servicio"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción del servicio",
                    "rows": 4,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Precio",
                    "min": "0",
                }
            ),
            "image_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://ejemplo.com/imagen.jpg",
                }
            ),
        }
