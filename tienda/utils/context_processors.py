from tienda.productos.models import *
from tienda.administrador.models import *


def categorias(request):
    """Devuelve las categorías de productos desde la base de datos."""
    categorias = Categoria.objects.all()  # Consulta todas las categorías de la base de datos
    return {'categorias': categorias}


# administrador/context_processors.py

def banners_context(request):
    """Devuelve los banners principales y secundarios desde el modelo."""
    return {
        'banners_principales': Banner.objects.filter(tipo='principal'),
        'banners_secundarios': Banner.objects.filter(tipo='secundario'),
    }
