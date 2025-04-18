from .models import *
from tienda.utils.decorators import *
from tienda.utils.validators import *
from tienda.productos.models import *
from tienda.usuarios.forms import PerfilUsuarioForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.messages import add_message, ERROR


#---------------------------------------------
    # USUARIO
#---------------------------------------------


def login(request):
    """Inicia sesión un usuario y redirige a la URL especificada en 'next'."""
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        next_url = request.POST.get('next', 'index')  # Por defecto redirige al index
        usuario = Usuario.objects.filter(correo=correo).first()
        if usuario and check_password(contrasena, usuario.contrasena):
            request.session['pista'] = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol
            }
            return redirect(next_url)  # Redirige a la URL especificada en next
        else:
            add_message(request, ERROR, 'Usuario o contraseña incorrectos', extra_tags='login_error')
            return redirect('index')
    else:
        return render(request, 'login_usuario.html')
    

def register(request):
    """Registra un nuevo usuario y lo inicia sesión automáticamente."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')
        next_url = request.POST.get('next', 'index')  # Default to 'index' if 'next' is empty
        if not next_url:  # Ensure next_url is not empty
            next_url = 'index'
        if contrasena != confirmar_contrasena:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect(next_url)
        try:
            usuario = Usuario(
                nombre=nombre,
                correo=correo,
                contrasena=make_password(contrasena)
            )
            usuario.save()
            request.session['pista'] = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol
            }
            messages.success(request, 'Usuario registrado e iniciado sesión correctamente')
            return redirect(next_url)
        except Exception as e:
            messages.error(request, f'Error al registrar el usuario: {e}')
            return redirect(next_url)
    else:
        next_url = request.GET.get('next', 'index')
        return render(request, 'registro_usuario.html', {'next': next_url})


def logout(request):
    """Cierra sesión del usuario y redirige a la URL de inicio."""
    try:
        del request.session['pista']
        return redirect('index')
    except:
        messages.error(request, 'Ocurrio un error')
        return redirect('index')
    

@session_rol_permission()
def profile(request):
    """"Muestra el perfil del usuario autenticado."""
    try:
        usuario = Usuario.objects.get(id=request.session['pista']['id'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login_usuario')

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("profile")),
        ("Perfil", reverse("profile"))
    ]

    context = {
        'usuario': usuario,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'usuario/perfil_usuario.html', context)


def update_profile(request):
    """Actualiza el perfil del usuario autenticado."""
    try:
        usuario = Usuario.objects.get(id=request.session['pista']['id'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login_usuario')

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = PerfilUsuarioForm(instance=usuario)

    # Verificar si el usuario tiene una imagen asociada
    imagen_perfil_url = usuario.imagen_perfil.url if usuario.imagen_perfil and hasattr(usuario.imagen_perfil, 'url') else None

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("profile")),
        ("Editar perfil", None)
    ]

    context = {
        'form': form,
        'usuario': usuario,
        'breadcrumbs': breadcrumbs,
        'imagen_perfil_url': imagen_perfil_url,
    }
    return render(request, 'usuario/editar_perfil_usuario.html', context)


def delete_profile(request):
    """"Elimina el perfil del usuario autenticado."""
    # try:
    #     usuario = Usuario.objects.get(id=request.session['pista']['id'])
    #     usuario.delete()
    #     del request.session['pista']
    #     messages.success(request, 'Cuenta eliminada correctamente')
    #     return redirect('index')
    # except Exception as e:
    #     messages.error(request, f'Error al eliminar la cuenta: {e}')
    #     return redirect('profile')

@session_rol_permission()
def address(request):
    """Muestra la dirección del usuario autenticado."""
    try:
        usuario = Usuario.objects.get(id=request.session['pista']['id'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login_usuario')
    
    direcciones = Direccion.objects.filter(usuario=usuario)
    
    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("profile")),
        ("Dirección", None)
    ]

    context = {
        'usuario': usuario,
        'breadcrumbs': breadcrumbs,
        'direcciones': direcciones,
    }
    return render(request, 'usuario/direccion_usuario.html', context)


def add_address(request):
    """"Agrega una nueva dirección para el usuario autenticado."""
    try:
        usuario = Usuario.objects.get(id=request.session['pista']['id'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login_usuario')

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("profile")),
        ("Dirección", reverse("address")),
        ("Agregar Dirección", None)
    ]

    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        estado = request.POST.get('estado')
        codigo_postal = request.POST.get('codigo_postal')
        pais = request.POST.get('pais')
        principal = request.POST.get('principal') == 'on'  # Verifica si el checkbox está marcado

        try:
            # Validar los datos de la dirección
            validar_direccion(direccion, ciudad, estado, codigo_postal, pais)

            # Crear la dirección
            nueva_direccion = Direccion.objects.create(
                usuario=usuario,
                direccion=direccion,
                ciudad=ciudad,
                estado=estado,
                codigo_postal=codigo_postal,
                pais=pais,
                principal=principal
            )
            messages.success(request, 'Dirección agregada correctamente.')
            return redirect('address')
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")


        # Si hay un error, devolver los datos ingresados al formulario
        return render(request, 'usuario/agregar_direccion_usuario.html', {
            'breadcrumbs': breadcrumbs,
            'direccion_valor': direccion,
            'ciudad_valor': ciudad,
            'estado_valor': estado,
            'codigo_postal_valor': codigo_postal,
            'pais_valor': pais,
            'principal_valor': principal,
        })
    
   

    # Para solicitudes GET, pasar valores vacíos al formulario
    return render(request, 'usuario/agregar_direccion_usuario.html', {
        'breadcrumbs': breadcrumbs,
        'direccion_valor': '',
        'ciudad_valor': '',
        'estado_valor': '',
        'codigo_postal_valor': '',
        'pais_valor': '',
        'principal_valor': False,
    })


@session_rol_permission()
def update_address(request,id_direccion):
    """"Actualiza una dirección existente del usuario autenticado."""
    try:
        direccion = Direccion.objects.get(id=id_direccion, usuario__id=request.session['pista']['id'])
    except Direccion.DoesNotExist:
        messages.error(request, "Dirección no encontrada.")
        return redirect('address')

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("profile")),
        ("Dirección", reverse("address")),
        ("Actualizar Dirección", None)
    ]

    if request.method == 'POST':
        direccion.direccion = request.POST.get('direccion')
        direccion.ciudad = request.POST.get('ciudad')
        direccion.estado = request.POST.get('estado')
        direccion.codigo_postal = request.POST.get('codigo_postal')
        direccion.pais = request.POST.get('pais')
        direccion.principal = request.POST.get('principal') == 'on'  # Verifica si el checkbox está marcado
        try:
            # Validar los datos de la dirección
            validar_direccion(direccion.direccion, direccion.ciudad, direccion.estado, direccion.codigo_postal, direccion.pais)
            # Guardar los cambios
            direccion.save()
            messages.success(request, 'Dirección actualizada correctamente.')
            return redirect('address')
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")

    return render(request, 'usuario/agregar_direccion_usuario.html', {
        'breadcrumbs': breadcrumbs,
        'direccion': direccion,
        'direccion_valor': direccion.direccion,
        'ciudad_valor': direccion.ciudad,
        'estado_valor': direccion.estado,
        'codigo_postal_valor': direccion.codigo_postal,
        'pais_valor': direccion.pais,
        'principal_valor': direccion.principal,
    })


def delete_address(request, id):
    """"Elimina una dirección existente del usuario autenticado."""
    try:
        direccion = Direccion.objects.get(id=id, usuario__id=request.session['pista']['id'])
        direccion.delete()
        messages.success(request, 'Dirección eliminada correctamente.')
    except Direccion.DoesNotExist:
        messages.error(request, "Dirección no encontrada.")
    except Exception as e:
        messages.error(request, f"Error inesperado: {e}")
    return redirect('address')


def set_primary_address(request, id_address):
    """Establece una dirección como principal."""
    try:
        direccion = Direccion.objects.get(id=id_address, usuario__id=request.session['pista']['id'])
        Direccion.objects.filter(usuario=direccion.usuario).update(principal=False)
        direccion.principal = True
        direccion.save()
        messages.success(request, 'Dirección establecida como principal.')
    except Direccion.DoesNotExist:
        messages.error(request, "Dirección no encontrada.")
    except Exception as e:
        messages.error(request, f"Error inesperado: {e}")
    return redirect('address')