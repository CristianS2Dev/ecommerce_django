from tienda.productos.models import *
from tienda.usuarios.models import *
from tienda.administrador.models import *
from django.shortcuts import render, redirect, get_object_or_404
from tienda.utils.decorators import *
from tienda.utils.validators import *
from django.contrib import messages




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
    context = {'data': q}
    return render(request, 'productos/lista_productos_admin.html', context)


@session_rol_permission(1)
def agregar_producto(request):
    """Agrega un nuevo producto."""
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio_original = request.POST.get("precio_original", "0")
        descuento = request.POST.get("descuento", "0")
        en_oferta = request.POST.get("en_oferta") == "on"
        sku = request.POST.get("sku")
        etiquetas_ids = request.POST.getlist("etiquetas")
        categoria_id = request.POST.get("categoria")
        marca_id = request.POST.get("marca")
        variantes = request.POST.getlist("variantes")  # Variantes enviadas como listas
        imagenes = request.FILES.getlist("imagenes")

        try:
            # Convertir y validar datos
            precio_original = Decimal(precio_original)
            descuento = Decimal(descuento)

            # Obtener instancias de relaciones
            categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
            marca = Marca.objects.get(id=marca_id) if marca_id else None

            # Crear el producto
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio_original=precio_original,
                descuento=descuento,
                en_oferta=en_oferta,
                categoria=categoria,
                marca=marca,
                sku=sku,
            )
            producto.save()

            # Guardar etiquetas asociadas al producto
            if etiquetas_ids:
                producto.etiquetas.set(etiquetas_ids)

            # Guardar variantes asociadas al producto
            for variante in request.POST.getlist("variantes[]"):
                color = variante.get("color")
                talla = variante.get("talla")
                stock = variante.get("stock", 0)
                Variante.objects.create(
                    producto=producto,
                    color=color,
                    talla=talla,
                    stock=stock,
                )

            # Guardar imágenes asociadas al producto
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, 'Producto agregado correctamente')
            return redirect('lista_productos_admin')  # Cambia a la URL adecuada
        except Categoria.DoesNotExist:
            messages.error(request, "La categoría seleccionada no existe.")
        except Marca.DoesNotExist:
            messages.error(request, "La marca seleccionada no existe.")
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        # Si ocurre un error, devolver los datos ingresados al formulario
        categorias = Categoria.objects.all()
        marcas = Marca.objects.all()
        etiquetas = Etiqueta.objects.all()

        return render(request, "productos/agregar_producto.html", {
            'categorias': categorias,
            'marcas': marcas,
            'nombre': nombre,
            'descripcion': descripcion,
            'precio_original': precio_original,
            'descuento': descuento,
            'en_oferta': en_oferta,
            'categoria_id': categoria_id,
            'marca_id': marca_id,
            'sku': sku,
            'etiquetas': etiquetas,
        })
    else:
        categorias = Categoria.objects.all()
        marcas = Marca.objects.all()
        etiquetas = Etiqueta.objects.all()

        return render(request, "productos/agregar_producto.html", {
            'categorias': categorias,
            'marcas': marcas,
            'etiquetas': etiquetas
        })

@session_rol_permission(1)
def editar_producto(request, id_producto):
    """Edita un producto existente."""
    try:
        producto = Producto.objects.get(pk=id_producto)
    except Producto.DoesNotExist:
        messages.error(request, "Producto no encontrado")
        return redirect('listar_productos')

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio_original = request.POST.get("precio_original", "0")
        descuento = request.POST.get("descuento", "0")
        en_oferta = request.POST.get("en_oferta") == "on"
        sku = request.POST.get("sku")
        etiquetas_ids = request.POST.getlist("etiquetas")  
        categoria_id = request.POST.get("categoria")
        marca_id = request.POST.get("marca")
        variantes = request.POST.get("variantes") 
        imagenes = request.FILES.getlist("imagenes")

        if producto.sku != sku:
            if Producto.objects.filter(sku=sku).exists():
                messages.error(request, "El SKU ya existe.")
                return redirect('editar_producto', id_producto=id_producto)
            else:
                producto.sku = sku

        try:
            precio_original = Decimal(precio_original)
            descuento = Decimal(descuento)

            categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
            marca = Marca.objects.get(id=marca_id) if marca_id else None

            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio_original = precio_original
            producto.descuento = descuento
            producto.en_oferta = en_oferta
            producto.categoria = categoria
            producto.marca = marca
            producto.sku = sku
            producto.save()

            if etiquetas_ids:
                producto.etiquetas.set(etiquetas_ids)

            if variantes:
                producto.variantes.all().delete()  
                for variante in json.loads(variantes): 
                    Variante.objects.create(
                        producto=producto,
                        color=variante.get("color"),
                        talla=variante.get("talla"),
                        stock=variante.get("stock", 0),
                    )

            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto actualizado correctamente")
            return redirect('lista_productos_admin')  # Cambia a la URL adecuada
        except Categoria.DoesNotExist:
            messages.error(request, "La categoría seleccionada no existe.")
        except Marca.DoesNotExist:
            messages.error(request, "La marca seleccionada no existe.")
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        categorias = Categoria.objects.all()
        marcas = Marca.objects.all()
        etiquetas = Etiqueta.objects.all()

        return render(request, "productos/agregar_producto.html", {
            'producto': producto,
            'categorias': categorias,
            'marcas': marcas,
            'etiquetas': etiquetas,
            'nombre': nombre,
            'descripcion': descripcion,
            'precio_original': precio_original,
            'descuento': descuento,
            'en_oferta': en_oferta,
            'categoria_id': categoria_id,
            'marca_id': marca_id,
            'etiquetas_ids': etiquetas_ids,
        })
    else:
        categorias = Categoria.objects.all()
        marcas = Marca.objects.all()
        etiquetas = Etiqueta.objects.all()
        variantes = producto.variantes.all()

        return render(request, "productos/agregar_producto.html", {
            'dato': producto, 
            'categorias': categorias,
            'marcas': marcas,
            'etiquetas': etiquetas,
            'variantes': variantes,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio_original': producto.precio_original,
            'descuento': producto.descuento,
            'en_oferta': producto.en_oferta,
            'categoria_id': producto.categoria.id if producto.categoria else None,
            'marca_id': producto.marca.id if producto.marca else None,
            'sku': producto.sku,
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
    context = {'data': q}
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
            return redirect('list_brands')  # Cambia a la URL adecuada
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

        try:
            # Actualizar la marca
            marca.nombre = nombre
            marca.descripcion = descripcion
            if logo:
                marca.logo = logo
            marca.save()
            messages.success(request, 'Marca actualizada correctamente')
            return redirect('list_brands')  # Cambia a la URL adecuada
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "marcas/editar_marca.html", {'marca': marca})


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