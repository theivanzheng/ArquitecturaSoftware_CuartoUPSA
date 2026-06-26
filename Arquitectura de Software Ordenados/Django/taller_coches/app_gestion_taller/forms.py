from django import forms
from .models import Cliente, Coche, Servicio, CocheServicio


class ClienteFormTradicional(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label='Nombre completo',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Ana García'}),
    )
    telefono = forms.CharField(
        max_length=15,
        label='Teléfono',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 600 000 000'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'Ej: ana@email.com'}),
    )

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()
        if not telefono.replace(' ', '').isdigit():
            raise forms.ValidationError('El teléfono solo puede contener dígitos.')
        return telefono

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un cliente con ese email.')
        return email


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Ana García'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 600 000 000'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ej: ana@email.com'}),
        }


class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = '__all__'
        labels = {
            'matricula': 'Matrícula',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'anio': 'Año',
            'cliente': 'Propietario',
        }
        widgets = {
            'matricula': forms.TextInput(attrs={'placeholder': 'Ej: 1234 ABC'}),
            'anio': forms.NumberInput(attrs={'min': 1900, 'max': 2030}),
        }


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'
        labels = {
            'descripcion': 'Descripción del servicio',
            'precio': 'Precio (€)',
            'fecha': 'Fecha',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej: Cambio de aceite'}),
        }


class CocheServicioForm(forms.ModelForm):
    class Meta:
        model = CocheServicio
        fields = '__all__'
        labels = {
            'coche': 'Coche',
            'servicio': 'Servicio',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones adicionales...'}),
        }
