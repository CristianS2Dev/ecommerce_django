from .models import *
from .forms import *
from tienda.utils.decorators import *
from tienda.productos.models import *
from tienda.utils.validators import *
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


# --- Vista de Productos ---

def products(request):
    """
    Vista para mostrar la lista de productos.
    """
    q = Producto.objects.all()
    context = {'data': q}
    return render(request, 'productos/productos.html', context)


def list_products(request):
    """
    Vista para mostrar la lista de productos con paginación.
    """
    productos = Producto.objects.all()

    nombre = request.GET.get('nombre')
    marca = request.GET.getlist('marca')
    etiquetas = request.GET.getlist('etiquetas')

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if etiquetas:
        productos = productos.filter(etiquetas__id__in=etiquetas).distinct()
    if marca:
        productos = productos.filter(marca__id__in=marca)

    # Paginación
    paginator = Paginator(productos, 9)  # 9 productos por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except Exception:
        page_obj = paginator.get_page(1)  # Si hay un error, mostrar la primera página

    contexto = {
        'data': page_obj,  # Cambiar 'productos' por 'data' para la paginación
        'nombre': nombre,
        'marca': marca,
        'etiquetas': etiquetas,
    }
    return render(request, 'productos/lista_productos.html', contexto)



def product_detail(request, id_producto):
    """Muestra los detalles de un producto."""
    producto = get_object_or_404(Producto, id=id_producto)
    variantes = producto.variantes.all()  # Obtener todas las variantes del producto

    # Generar un rango de cantidades basado en el stock total del producto
    rango_cantidad = range(1, producto.stock + 1) if producto.stock > 0 else []

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'variantes': variantes,  # Pasar las variantes al contexto
        'rango_cantidad': rango_cantidad,  # Pasar el rango de cantidades
    })


def products_by_category(request, id_categoria):
    """
    Vista para mostrar productos por categoría.
    """
    categoria = get_object_or_404(Categoria, id=id_categoria)
    productos = Producto.objects.filter(categoria=categoria)

    nombre = request.GET.get('nombre')
    marca = request.GET.getlist('marca')
    etiquetas = request.GET.getlist('etiquetas')

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if etiquetas:
        productos = productos.filter(etiquetas__id__in=etiquetas).distinct()
    if marca:
        productos = productos.filter(marca__id__in=marca)

    # Paginación
    paginator = Paginator(productos, 9)  # 9 productos por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except Exception:
        page_obj = paginator.get_page(1)  # Si hay un error, mostrar la primera página

    contexto = {
        'data': page_obj,  # Cambiar 'productos' por 'data' para la paginación
        'categoria': categoria.nombre,  # Usar el nombre de la categoría
    }
    return render(request, 'productos/productos_por_categoria.html', contexto)