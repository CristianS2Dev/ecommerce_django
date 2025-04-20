from tienda.productos.models import *
from tienda.usuarios.models import *
from tienda.administrador.models import *
from django.shortcuts import render, redirect, get_object_or_404
from tienda.utils.decorators import *
from tienda.utils.validators import *
from django.contrib import messages
from .forms import VarianteForm 
import json
from django.core.paginator import Paginator
from tienda.administrador.forms import ProductoForm, VarianteFormSet



#---------------------------------------------
    # ADMINISTRADOR
#---------------------------------------------

def login(request):
    """Inicia sesión un administrador y redirige a la URL especificada."""
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        usuario = Usuario.objects.filter(correo=correo, contrasena=contrasena).first()
        if usuario:
            request.session['pista'] = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol
            }
            if usuario.rol == 1:
                return redirect('administrador')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')
    else:
        return render(request, 'login_admin.html')


def logout(request):
    try:
        del request.session['pista']
        return redirect('index')
    except:
        messages.error(request, 'Ocurrio un error')
        return redirect('index')
    

@session_rol_permission(1)
def dashboard_admin(request):
    """Muestra el panel de administración."""
    q = Producto.objects.all()
    context = {'data': q}
    return render(request, 'index_admin.html', context)



def lista_productos_admin(request):
    """Lista todos los productos en la vista de administración."""
    q = Producto.objects.all()
    variantes = Variante.objects.all()
    paginator = Paginator(q, 10)  # Cambia el número de productos por página según sea necesario
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'data': q,
               'variantes': variantes,
               'page_obj': page_obj,
               'paginator': paginator,}
    return render(request, 'productos/lista_productos_admin.html', context)


@session_rol_permission(1)
def agregar_producto(request):
    """Agrega un nuevo producto."""
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    etiquetas = Etiqueta.objects.all()

    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            try:
                producto = form.save(commit=False)
                producto.save()

                # Guardar etiquetas
                etiquetas_ids = request.POST.getlist("etiquetas")
                if etiquetas_ids:
                    producto.etiquetas.set(etiquetas_ids)

                # Guardar variantes
                formset = VarianteFormSet(request.POST, instance=producto)
                if formset.is_valid():
                    formset.save()
                else:
                    for i, formset_error in enumerate(formset.errors):
                        for field, error in formset_error.items():
                            messages.error(request, f"Error en variante {i+1} - '{field}': {error}")
                    messages.error(request, "Hay errores en el formulario de variantes.")
                    return render(request, "productos/agregar_producto.html", {
                        'form': form,
                        'formset': formset,
                        'categorias': categorias,
                        'marcas': marcas,
                        'etiquetas': etiquetas,
                    })

                # Guardar imágenes
                imagenes = request.FILES.getlist("imagenes")
                for imagen in imagenes:
                    ImagenProducto.objects.create(producto=producto, imagen=imagen)

                messages.success(request, 'Producto agregado correctamente')
                return redirect('lista_productos_admin')
            except Exception as e:
                messages.error(request, f"Error: {e}")
                formset = VarianteFormSet(request.POST)  # sin instancia
        else:
            # Si el form no es válido, crea el formset sin instancia
            formset = VarianteFormSet(request.POST)

            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error en '{field}': {error}")

        return render(request, "productos/agregar_producto.html", {
            'form': form,
            'formset': formset,
            'categorias': categorias,
            'marcas': marcas,
            'etiquetas': etiquetas,
        })

    else:
        form = ProductoForm()
        formset = VarianteFormSet()

    return render(request, "productos/agregar_producto.html", {
        'form': form,
        'formset': formset,
        'categorias': categorias,
        'marcas': marcas,
        'etiquetas': etiquetas,
    })


@session_rol_permission(1)
def editar_producto(request, id_producto):
    """Edita un producto existente."""
    try:
        producto = Producto.objects.get(pk=id_producto)
    except Producto.DoesNotExist:
        messages.error(request, "Producto no encontrado")
        return redirect('lista_productos_admin')

    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    etiquetas = Etiqueta.objects.all()

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        formset = VarianteFormSet(request.POST or None, instance=producto)

        if form.is_valid() and formset.is_valid():
            try:
                form.save()

                # Actualizar etiquetas
                etiquetas_ids = request.POST.getlist("etiquetas")
                producto.etiquetas.set(etiquetas_ids)

                # Guardar variantes (sin borrar)
                formset.save()

                # Agregar nuevas imágenes
                imagenes = request.FILES.getlist("imagenes")
                for imagen in imagenes:
                    ImagenProducto.objects.create(producto=producto, imagen=imagen)

                messages.success(request, "Producto actualizado correctamente")
                return redirect('lista_productos_admin')
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
           # Mostrar errores específicos de los formularios
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error en '{field}': {error}")
            if formset.errors:
                for i, formset_error in enumerate(formset.errors):
                    for field, error in formset_error.items():
                        messages.error(request, f"Error en variante {i+1} - '{field}': {error}")
            messages.error(request, "Hay errores en el formulario.")
    else:
        form = ProductoForm(instance=producto)
        formset = VarianteFormSet(instance=producto)

    return render(request, "productos/agregar_producto.html", {
        'form': form,
        'formset': formset,
        'dato': producto,
        'categorias': categorias,
        'marcas': marcas,
        'etiquetas': etiquetas,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'precio_original': producto.precio_original,
        'descuento': producto.descuento,
        'en_oferta': producto.en_oferta,
        'sku': producto.sku,
        'categoria_id': producto.categoria.id if producto.categoria else None,
        'marca_id': producto.marca.id if producto.marca else None,
        'etiquetas_ids': producto.etiquetas.values_list('id', flat=True),
    })


@session_rol_permission(1)
def eliminar_producto(request, id_producto):
    """Elimina un producto."""
    try:
        q: Producto = Producto.objects.get(id=id_producto)
        q.delete()
        messages.success(request, 'Producto eliminado correctamente')
    except Producto.DoesNotExist:
        messages.error(request, 'Producto no encontrado')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('lista_productos_admin')


@session_rol_permission(1)
def list_brands(request):
    """Lista todas las marcas."""
    q = Marca.objects.all()
    context = {'marcas': q}  
    return render(request, 'marcas/lista_marcas_admin.html', context)


@session_rol_permission(1)
def add_brand(request):
    """Agrega una nueva marca."""
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        logo = request.FILES.get("logo")

        try:
            # Crear la marca
            marca = Marca(nombre=nombre, descripcion=descripcion, logo=logo)
            marca.save()
            messages.success(request, 'Marca agregada correctamente')
            return redirect('list_brands') 
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "marcas/agregar_marca.html")


@session_rol_permission(1)
def edit_brand(request, brand_id):
    """Edita una marca existente."""
    try:
        marca = Marca.objects.get(pk=brand_id)
    except Marca.DoesNotExist:
        messages.error(request, "Marca no encontrada")
        return redirect('list_brands')

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        logo = request.FILES.get("logo")
        visible = request.POST.get("visible") == "on" 

        try:
            marca.nombre = nombre
            marca.descripcion = descripcion
            marca.visible = visible 
            if logo:
                marca.logo = logo
            marca.save()
            messages.success(request, 'Marca actualizada correctamente')
            return redirect('list_brands')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "marcas/agregar_marca.html", {'marca': marca})


@session_rol_permission(1)
def delete_brand(request, brand_id):
    """Elimina una marca."""
    try:
        q: Marca = Marca.objects.get(id=brand_id)
        q.delete()
        messages.success(request, 'Marca eliminada correctamente')
    except Marca.DoesNotExist:
        messages.error(request, 'Marca no encontrada')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('list_brands')


@session_rol_permission(1)
def list_banners(request):
    """Lista todos los banners."""
    banners = Banner.objects.all()  
    context = {'banners': banners}  
    return render(request, 'banners/listar_banners.html', context)


@session_rol_permission(1)
def add_banner(request):
    """Agrega un nuevo banner."""
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        imagen = request.FILES.get("imagen")
        tipo = request.POST.get("tipo")

        try:
            if tipo == 'secundario' and Banner.objects.filter(tipo='secundario').exists():
                raise ValidationError("Solo se permite un banner secundario. Elimine el existente para agregar uno nuevo.")
            if not imagen:
                raise ValidationError("Debe subir una imagen para el banner.")
            # Crear el banner
            banner = Banner(
                titulo=titulo,
                imagen=imagen,
                tipo=tipo,
            )
            banner.save()
            messages.success(request, 'Banner agregado correctamente.')
            return redirect('list_banners')
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")
        return redirect('add_banner')
    else:
        return render(request, 'banners/agregar_banner.html')
    

@session_rol_permission(1)
def edit_banner(request, banner_id):
    """Edita un banner existente."""
    banner = get_object_or_404(Banner, pk=banner_id)
    if request.method == "POST":
        try:
            nueva_imagen = request.FILES.get("imagen")
            banner.titulo = request.POST.get("titulo")
            banner.tipo = request.POST.get("tipo")

            if nueva_imagen:
                banner.imagen = nueva_imagen
            banner.save()
            messages.success(request, 'Banner actualizado correctamente')
            return redirect('list_banners')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "banners/editar_banner.html", {'banner': banner})


@session_rol_permission(1)
def delete_banner(request, banner_id):
    """Elimina un banner."""
    try:
        q: Banner = Banner.objects.get(id=banner_id)
        q.delete()
        messages.success(request, 'Banner eliminado correctamente')
    except Banner.DoesNotExist:
        messages.error(request, 'Banner no encontrado')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('list_banners')


@session_rol_permission(1)
def list_variants(request):
    """Lista todas las variantes de productos."""
    variantes = Variante.objects.select_related('producto').all()
    context = {'variantes': variantes}
    return render(request, 'productos/variantes/lista_variantes_admin.html', context)



@session_rol_permission(1)
def add_variant(request, id_producto):
    """
    Vista para agregar una nueva variante a un producto.
    """
    producto = get_object_or_404(Producto, id=id_producto)

    if request.method == 'POST':
        form = VarianteForm(request.POST)
        if form.is_valid():
            variante = form.save(commit=False)
            variante.producto = producto
            variante.save()
            messages.success(request, 'Variante agregada exitosamente.')
            return redirect('list_variants', id_producto=producto.id)
    else:
        form = VarianteForm()

    return render(request, 'productos/variantes/agregar_variante.html', {
        'form': form,
        'producto': producto,
    })


@session_rol_permission(1)
def edit_variant(request, id_variante):
    """
    Vista para editar una variante existente.
    """
    variante = get_object_or_404(Variante, id=id_variante)
    producto = variante.producto

    if request.method == 'POST':
        form = VarianteForm(request.POST, instance=variante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Variante actualizada exitosamente.')
            return redirect('list_variants', id_producto=producto.id)
    else:
        form = VarianteForm(instance=variante)

    return render(request, 'productos/variantes/agregar_variante.html', {
        'form': form,
        'producto': producto,
        'variante': variante,
    })


@session_rol_permission(1)
def delete_variant(request, variant_id):
    """Elimina una variante."""
    try:
        q: Variante = Variante.objects.get(id=variant_id)
        q.delete()
        messages.success(request, 'Variante eliminada correctamente')
    except Variante.DoesNotExist:
        messages.error(request, 'Variante no encontrada')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('list_variants')
