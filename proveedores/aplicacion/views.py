from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ProveedorForm, ProductoForm, PrecioProductoForm
from .models import Proveedor, Producto, PrecioProducto
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.db import IntegrityError
from django.db.models import OuterRef, Subquery, Max, DecimalField,  Value, F
from django.db.models.functions import  Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages





def index(request):
    context = {}
    proveedores = Proveedor.objects.all().order_by("nombre")
    context["proveedores"]= proveedores
    return render(request, 'aplicacion/index.html', context)

def proveedor_list(request):
    q = request.GET.get('q', '')  # Obtener el parámetro de búsqueda
    proveedores_list = Proveedor.objects.filter(nombre__icontains=q).order_by("nombre")

    # Configurar la paginación
    paginator = Paginator(proveedores_list, 15)  # Mostrar 20 proveedores por página
    page = request.GET.get('page')

    try:
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        proveedores = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por encima del número total de páginas),
        # mostrar la última página
        proveedores = paginator.page(paginator.num_pages)

    return render(request, 'aplicacion/proveedor_list.html', {'proveedores': proveedores, 'q': q})

def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save(commit=False)
            while True:
                try:
                    proveedor.save()
                    messages.success(request, 'Proveedor creado exitosamente.')
                    break
                except IntegrityError:
                    proveedor.id = None
            # Limpiar el formulario después de guardar con éxito
            form = ProveedorForm()
            return render(request, 'aplicacion/proveedor_form.html', {'form': form, 'is_update': False})
    else:
        # Método GET: Retorna el formulario vacío para mostrar en la página
        form = ProveedorForm()
        return render(request, 'aplicacion/proveedor_form.html', {'form': form, 'is_update': False})

    


def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor-list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'aplicacion/proveedor_form.html', {'form': form, 'is_update': True})

def proveedor_productos(request, proveedor_id):
    # Obtener el proveedor por su ID
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)

    # Subconsulta para obtener el precio más reciente para cada producto y proveedor
    subquery = PrecioProducto.objects.filter(
        producto=OuterRef('id'),
        proveedor=proveedor
    ).order_by('-fecha_actualizacion').values('precio_actual')[:1]

    # Consulta principal para obtener los productos con sus precios más recientes
    productos_con_precios_actuales = Producto.objects.annotate(
        precio_actual=Coalesce(Subquery(subquery), Value(Decimal('0.0'), output_field=DecimalField()))
    ).filter(proveedores=proveedor).distinct()

    return render(request, 'aplicacion/proveedor_productos.html', {'proveedor': proveedor, 'productos_con_precios_actuales': productos_con_precios_actuales})

@require_POST
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    return redirect('proveedor-list')

def producto_list(request):
    q = request.GET.get('q', '')  # Obtener el parámetro de búsqueda
    productos_list = Producto.objects.filter(nombre__icontains=q).order_by("nombre")

    # Configurar la paginación
    paginator = Paginator(productos_list, 20)  # Mostrar 20 proveedores por página
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        productos = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por encima del número total de páginas),
        # mostrar la última página
        productos = paginator.page(paginator.num_pages)

    return render(request, 'aplicacion/producto_list.html', {'productos': productos, 'q': q})

def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            while True:
                try:
                    producto.save()
                    messages.success(request, 'Producto creado exitosamente.')
                    break
                except IntegrityError:
                    producto.id = None
            # Limpiar el formulario después de guardar con éxito
            form = ProductoForm()
    else:
        form = ProductoForm()

    return render(request, 'aplicacion/producto_form.html', {'form': form})



def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto-list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'aplicacion/producto_form.html', {'form': form, 'is_update': True})

@require_POST
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('producto-list')


def productos_proveedor(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Consulta para obtener el precio más reciente de cada proveedor para el producto dado
    proveedores_con_precios = PrecioProducto.objects.filter(producto=producto).values(
        'proveedor__nombre',
        'precio_actual',
        'fecha_actualizacion'
    ).order_by('proveedor', '-fecha_actualizacion').distinct('proveedor')

    return render(request, 'aplicacion/productos_proveedor.html', {'producto': producto, 'proveedores_con_precios': proveedores_con_precios})

def precio_producto_list(request):
    q = request.GET.get('q', '')
    
    # Subconsulta para obtener el precio más reciente para cada producto y proveedor
    subquery = PrecioProducto.objects.filter(
        producto=OuterRef('producto'),
        proveedor=OuterRef('proveedor')
    ).order_by('-fecha_actualizacion').values('precio_actual')[:1]

    # Consulta principal para obtener los precios más recientes
    precios = PrecioProducto.objects.annotate(
        ultima_fecha=Max('fecha_actualizacion'),
        resultado=Coalesce(Subquery(subquery), Decimal('0.0'))
    ).filter(
        fecha_actualizacion=F('ultima_fecha'),
        precio_actual=F('resultado'),
        producto__nombre__icontains=q  # Aplicar filtro por nombre de producto
    ).order_by('producto__nombre', 'proveedor__nombre')  # Ordenar alfabéticamente por nombre de producto y nombre de proveedor

    return render(request, 'aplicacion/precio_producto_list.html', {'precios': precios, 'q': q})
def precio_producto_create(request):
    productos_ordenados = Producto.objects.all().order_by('nombre')

    if request.method == 'POST':
        form = PrecioProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('precio-list')
    else:
        form = PrecioProductoForm()

    return render(request, 'aplicacion/precio_producto_form.html', {'form': form, 'productos': productos_ordenados})



def precio_producto_update(request, pk):
    precio_producto = get_object_or_404(PrecioProducto, pk=pk)
    if request.method == 'POST':
        form = PrecioProductoForm(request.POST, instance=precio_producto)
        if form.is_valid():
            form.save()
            return redirect('precio-list')
    else:
        form = PrecioProductoForm(instance=precio_producto)
    return render(request, 'aplicacion/precio_producto_form.html', {'form': form, 'is_update': True})


@require_POST
def precio_producto_delete(request, pk):
    precio_producto = get_object_or_404(PrecioProducto, pk=pk)
    precio_producto.delete()
    return redirect('precio-list')


def precio_producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, nombre=producto_id)
    proveedores = producto.proveedores.all()

    # Obtén todos los precios ordenados por fecha de actualización descendente
    precios = PrecioProducto.objects.filter(proveedor__in=proveedores).order_by('-fecha_actualizacion')

    # Configura el paginador con 20 precios por página
    paginator = Paginator(precios, 20)
    page = request.GET.get('page')

    try:
        precios_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        precios_pagina = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por encima del número total de páginas), muestra la última página
        precios_pagina = paginator.page(paginator.num_pages)

    return render(request, 'aplicacion/precio_producto_detalle.html', {'producto': producto, 'precios_pagina': precios_pagina})

def buscar_productos(request):
    query = request.GET.get('q', '')
    resultados = Producto.objects.filter(nombre__icontains=query).values('id', 'nombre')
    return JsonResponse(list(resultados), safe=False)