# proveedores/admin.py
from django.contrib import admin
from .models import Proveedor, Producto, PrecioProducto

admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(PrecioProducto)
