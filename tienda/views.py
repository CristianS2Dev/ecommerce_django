from django.shortcuts import render
from tienda.productos.models import *
from .templatetags.custom_filters import *
from .templatetags.breadcrumbs import *

def index(request):
    q = Producto.objects.all()
    marcas = Marca.objects.filter(visible=True)[:6]
    # banners_principales = Banner.objects.filter(tipo='principal')
    # banners_secundarios = Banner.objects.filter(tipo='secundario')
    context = {'data': q,
               'marcas': marcas,
            #    'banners_principales': banners_principales,
            #    'banners_secundarios': banners_secundarios
            }
    return render(request, 'tienda/index.html', context)
