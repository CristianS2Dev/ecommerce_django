from tienda.carrito.models import *
from tienda.productos.models import *
from tienda.usuarios.models import Usuario
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tienda.utils.decorators import *
from django.db.models import F



def get_cart(request):
    """Obtiene el carrito del usuario autenticado o de la sesión."""
    if request.session.get('pista'):  # Usuario autenticado
        usuario = Usuario.objects.filter(id=request.session['pista']['id']).first()
        if not usuario:
            raise ValueError("El usuario autenticado no está registrado.")
        carrito, _ = Carrito.objects.get_or_create(usuario=usuario)

        # Combinar carrito de sesión con el del usuario autenticado
        session_carrito_id = request.session.get('carrito_id')
        if session_carrito_id:
            session_carrito = Carrito.objects.filter(id=session_carrito_id).first()
            if session_carrito:
                for elemento in session_carrito.elementos.all():
                    elemento.carrito = carrito
                    elemento.save()
                session_carrito.delete()
                del request.session['carrito_id']
    else:  # Usuario no autenticado
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id).first()
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    return carrito



def cart(request):
    """Vista para mostrar el carrito de compras."""
    carrito = get_cart(request)
    elementos = carrito.elementos.all()
    total = carrito.total()  # Usa el método `total` del modelo Carrito

    contexto = {
        'elementos': elementos,
        'total': total,
    }
    return render(request, 'carrito.html', contexto)


def add_item(request, id_producto):
    """Vista para agregar un producto al carrito de compras."""
    try:
        carrito = get_cart(request)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('carrito')

    producto = get_object_or_404(Producto, id=id_producto)
    cantidad = int(request.POST.get('cantidad', 1))
    color = request.POST.get('color')
    talla = request.POST.get('tamano')

    # Validar que se haya seleccionado un color y una talla
    if not color or not talla:
        messages.error(request, "Debes seleccionar un color y una talla.")
        return redirect('product_detail', id_producto=id_producto)

    # Buscar la variante correspondiente
    variante = producto.variantes.filter(color=color, talla=talla).first()
    if not variante:
        messages.error(request, "La variante seleccionada no está disponible.")
        return redirect('product_detail', id_producto=id_producto)

    # Validar el stock de la variante
    if cantidad > variante.stock:
        messages.error(request, "La cantidad excede el stock disponible para esta variante.")
        return redirect('product_detail', id_producto=id_producto)

    # Crear o actualizar el elemento en el carrito
    elemento, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=producto, variante=variante)
    if not creado:
        if elemento.cantidad + cantidad > variante.stock:
            messages.error(request, "La cantidad total excede el stock disponible para esta variante.")
            return redirect('carrito')
        elemento.cantidad += cantidad
    else:
        elemento.cantidad = cantidad
    elemento.save()

    messages.success(request, f"{producto.nombre} ({color}, {talla}) agregado al carrito.")
    return redirect('carrito')

def update_item(request, id_elemento):
    """Actualiza la cantidad de un producto en el carrito."""
    if request.method == 'POST':
        carrito = get_cart(request)
        elemento = get_object_or_404(ElementoCarrito, id=id_elemento, carrito=carrito)
        nueva_cantidad = int(request.POST.get('cantidad', 1))

        # Validar la cantidad
        if nueva_cantidad <= 0:
            elemento.delete()
            total = carrito.total()
            return JsonResponse({'subtotal': 0, 'total': total})

        if nueva_cantidad > elemento.producto.stock:
            return JsonResponse({'error': 'La cantidad excede el stock disponible.'}, status=400)

        # Actualizar la cantidad
        elemento.cantidad = nueva_cantidad
        elemento.save()

        # Calcular el subtotal y el total del carrito
        subtotal = elemento.subtotal()
        total = carrito.total()

        return JsonResponse({'subtotal': subtotal, 'total': total})

    return JsonResponse({'error': 'Método no permitido'}, status=405)



def remove_item(request, id_producto):
    """Vista para eliminar un producto del carrito de compras."""
    carrito = get_cart(request)
    producto = get_object_or_404(Producto, id=id_producto)
    elemento = ElementoCarrito.objects.filter(carrito=carrito, producto=producto).first()

    if elemento:
        elemento.delete()
        messages.success(request, f"{producto.nombre} eliminado del carrito.")
    else:
        messages.error(request, "El producto no está en el carrito.")

    return redirect('carrito')


@session_rol_permission()
def checkout_cart(request):
    """Vista para el proceso de checkout del carrito de compras."""
    if not request.session.get('pista'):
        messages.error(request, "Debes iniciar sesión para proceder al pago.")
        return redirect('login_usuario')

    carrito = get_cart(request)

    if not carrito.elementos.exists():
        messages.error(request, "El carrito está vacío.")
        return redirect('carrito')

    # Validar stock antes de procesar el pago
    for elemento in carrito.elementos.all():
        if elemento.cantidad > elemento.producto.stock:
            messages.error(request, f"Stock insuficiente para {elemento.producto.nombre}.")
            return redirect('carrito')

    # Procesar el pago
    total = carrito.total()
    messages.success(request, f"Pago procesado correctamente. Total: {total}")

    # Actualizar el stock y limpiar el carrito
    for elemento in carrito.elementos.all():
        elemento.producto.stock = F('stock') - elemento.cantidad
        elemento.producto.save()
        elemento.delete()

    return redirect('index')
