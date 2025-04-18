from .models import *
from .forms import *
from tienda.utils.decorators import *
from tienda.productos.models import *
from tienda.utils.validators import *
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


# --- Vista de Productos ---



from django.db.models import Q

def list_products(request, id_categoria=None):
    """
    Vista para mostrar la lista de productos con filtros opcionales.
    Si se proporciona una categoría, filtra los productos por esa categoría.
    """
    productos = Producto.objects.all()
    colores_disponibles = Variante.objects.values('color').distinct()

    categoria = None
    if id_categoria:
        categoria = get_object_or_404(Categoria, id=id_categoria)
        productos = productos.filter(categoria=categoria)

    nombre = request.GET.get('nombre')
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)

    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    marca_id = request.GET.get('marca')
    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    colores = request.GET.getlist('color')
    if colores:
        productos = productos.filter(variantes__color__in=colores).distinct()

    # Ordenar productos
    orden = request.GET.get('orden')
    if orden == 'popular':
        productos = productos.order_by('-id')  # Cambia según tu lógica de popularidad
    elif orden == 'barato':
        productos = productos.order_by('precio')
    elif orden == 'caro':
        productos = productos.order_by('-precio')

    # Paginación
    paginator = Paginator(productos, 9)  # 9 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto para la plantilla
    contexto = {
        'data': page_obj,
        'categoria': categoria,
        'categorias': Categoria.objects.all(),
        'marcas_disponibles': Marca.objects.all(),
        'colores_disponibles': colores_disponibles,
    }
    return render(request, 'productos/lista_productos.html', contexto)

def product_detail(request, id_producto):
    """Muestra los detalles de un producto."""
    producto = get_object_or_404(Producto, id=id_producto)
    variantes = producto.variantes.all()  # Obtener todas las variantes del producto

    # Obtener el stock del primer variante disponible
    stockid = None
    for variante in variantes:
        if variante.stock > 0:
            stockid = variante.stock
            break

    # Generar el rango de cantidades si hay stock
    cantidad_rango = range(1, stockid + 1) if stockid else []

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'variantes': variantes,  # Pasar las variantes al contexto
        'cantidad_rango': cantidad_rango,  # Pasar el rango de cantidades al contexto
    })




