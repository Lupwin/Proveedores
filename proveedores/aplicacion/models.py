from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Proveedores"  # Corregido el nombre en plural
        verbose_name = "Proveedor"

    
    

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    proveedores = models.ManyToManyField(Proveedor, through='PrecioProducto', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Productos"
        verbose_name = "Producto"

        


class PrecioProducto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='precios')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=4)
    fecha_actualizacion = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.producto} - {self.proveedor} - {self.precio_actual}"

