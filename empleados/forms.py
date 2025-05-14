from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Select
from django import forms
from .models import Empleado, Cargo, Departamento, TipoContrato, Rol, BonificacionExtra


class EmpleadoForm(ModelForm):
    def clean_cedula(self):
            cedula = self.cleaned_data.get('cedula')

            if not cedula.isdigit():
                raise forms.ValidationError("La cédula debe contener solo números.")
            
            if len(cedula) != 10:
                raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")

            return cedula
    class Meta:
        model = Empleado
        # fields = ['name',' email','phone','cargo']
        #cada campo lo convierte a un control html <input type="text" name="name" id="name" class="form-control" placeholder="Nombre del empleado" required>
        fields = '__all__'
        # exclude = ['phone']
        

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del empleado', 'required': 'required'}),
            'cedula': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cédula', 'required': 'required'}),
            'cargo': Select(attrs={'class': 'form-control', 'placeholder': 'Cargo', 'required': 'required'}),
            'direccion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'required': 'required'}),
            'sexo': Select(attrs={'class': 'form-control', 'placeholder': 'Sexo', 'required': 'required'}),
            'sueldo': TextInput(attrs={'class': 'form-control', 'placeholder': 'Sueldo', 'required': 'required'}),
            'departamento': Select(attrs={'class': 'form-control', 'placeholder': 'Departamento', 'required': 'required'}),
            'tipo_contrato': Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de contrato', 'required': 'required'}),
        }

class CargoForm(ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'required': 'required'}),
        }
class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'required': 'required'}),
        }

class ContratoForm(ModelForm):
    class Meta:
        model = TipoContrato
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'required': 'required'}),
        }

class RolForm(ModelForm):
    class Meta:
        model = Rol
        fields = ['empleado', 'aniomes', 'horas_extra', 'bono']
        # exclude = ['iess', 'tot_ing', 'tot_des', 'neto']
        # Esto es para que no se muestren los campos iess, tot_ing, tot_des y neto en el formulario
        # ya que estos se calculan automáticamente en el modelo
        widgets = {
            'empleado': Select(attrs={'class': 'form-control'}),
            'aniomes': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            #'sueldo': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas_extra': forms.NumberInput(attrs={'class': 'form-control'}),
            'bono': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BonificacionForm(ModelForm):
    class Meta:
        model = BonificacionExtra
        fields = ['rol', 'descripcion', 'monto']
        widgets = {
            'rol': Select(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'required': 'required'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
        }
