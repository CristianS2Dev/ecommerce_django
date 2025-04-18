from django.core.exceptions import ValidationError


# ---------------------------------------------
    # Validaciones
# ---------------------------------------------

def validar_num_negativo(stock, precio_original, descuento):
    """Valida que los números no sean negativos. Lanza una excepción si falla."""
    errores = []
    if stock < 0:
        errores.append("El stock no puede ser negativo.")
    if precio_original < 0:
        errores.append("El precio original no puede ser negativo.")
    if descuento < 0:
        errores.append("El descuento no puede ser negativo.")
    
    if errores:
        raise ValidationError(errores)


def validar_archivo(imagen, formatos_permitidos=None):
    """Valida el tipo de archivo permitido."""
    if formatos_permitidos is None:
        formatos_permitidos = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if imagen.content_type not in formatos_permitidos:
        raise ValidationError(f"Formato no permitido: {imagen.content_type}. Solo se aceptan: {', '.join(formatos_permitidos)}.")


def validar_tamano_archivo(imagen, max_size_mb=5):
    """Valida el tamaño del archivo subido."""
    if imagen.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"El archivo '{imagen.name}' excede el tamaño máximo permitido de {max_size_mb} MB. Tamaño actual: {imagen.size / (1024 * 1024):.2f} MB.")


def validar_imagen(imagen, max_size_mb=5, formatos_permitidos=None):
    """Valida el tipo y tamaño del archivo subido."""
    try:
        validar_archivo(imagen, formatos_permitidos)
        validar_tamano_archivo(imagen, max_size_mb)
    except ValidationError as ve:
        raise ValidationError(f"Error de validación en el archivo '{imagen.name}': {ve}")
    except Exception as e:
        raise Exception(f"Error inesperado al validar el archivo '{imagen.name}': {e}")


def validar_direccion(direccion, ciudad, estado, codigo_postal, pais):
    """Valida los campos de una dirección."""
    if not all([direccion, ciudad, estado, codigo_postal, pais]):
        raise ValidationError("Todos los campos son obligatorios.")
    if not codigo_postal.isdigit() or len(codigo_postal) != 6:
        raise ValidationError("El código postal debe ser un número de 5 dígitos.")
    

