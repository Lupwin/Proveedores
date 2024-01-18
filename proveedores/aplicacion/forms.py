from django import forms
from .models import Proveedor, Producto, PrecioProducto
from django.core.exceptions import ValidationError


          
class ProveedorForm(forms.ModelForm):
    def clean_nombre(self):
        data = self.cleaned_data["nombre"]
        if Proveedor.objects.filter(nombre=data):
            raise ValidationError('El proveedor que esta ingresando, ya es esta registrado')
        return data   
    
    class Meta: 
        model = Proveedor
        fields = ['nombre']
        
class ProductoForm(forms.ModelForm):
    def clean_nombre(self):
        # Validación del campo nombre
        nombre = self.cleaned_data["nombre"]
        
        if Producto.objects.filter(nombre=nombre).exists():
            raise ValidationError('El producto que está ingresando ya está registrado.')

        return nombre

    class Meta:
        model = Producto
        fields = ['nombre', 'proveedores']


class PrecioProductoForm(forms.ModelForm):
    class Meta:
        model = PrecioProducto
        fields = ['proveedor', 'producto', 'precio_actual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].widget.attrs['id'] = 'id_producto'


class BuscarProductoForm(forms.Form):
    producto_nombre = forms.CharField(max_length=255, required=False, label='Nombre del Producto')