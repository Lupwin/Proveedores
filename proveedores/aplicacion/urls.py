from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('proveedores/', views.proveedor_list, name='proveedor-list'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor-create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor-update'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor-delete'),
    path('proveedor_productos/<int:proveedor_id>/', views.proveedor_productos, name='proveedor_productos'),

    path('productos/', views.producto_list, name='producto-list'),
    path('productos/nuevo/', views.producto_create, name='producto-create'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto-update'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto-delete'),
    path('productos_proveedor/<int:producto_id>/', views.productos_proveedor, name='productos_proveedor'),
    path('buscar-productos/', views.buscar_productos, name='buscar-productos'),
    
    path('precios/', views.precio_producto_list, name='precio-list'),
    path('precios/nuevo/', views.precio_producto_create, name='precio-create'),
    path('precios/<int:pk>/editar/', views.precio_producto_update, name='precio-update'),
    path('precios/<int:pk>/eliminar/', views.precio_producto_delete, name='precio-delete'),
    path('precio_producto_detalle/<str:producto_id>/', views.precio_producto_detalle, name='precio_producto_detalle'),
]
