from django.contrib import messages
from django.shortcuts import redirect

def session_rol_permission(*roles):
    """
    Decorator to enforce role-based access control for views using session data.

    This decorator checks if a user is authenticated and has the required role(s)
    to access a specific view. If the user is not authenticated or does not have
    the required role, they are redirected to the appropriate page with a message.

    Args:
        *roles: A variable-length argument list of roles that are allowed to access
                the decorated view. If no roles are specified, any authenticated
                user is allowed.

    Returns:
        A decorator function that wraps the original view function.

    Behavior:
        - If the user is authenticated and their role matches one of the specified
          roles (or no roles are specified), the original view function is executed.
        - If the user is authenticated but their role does not match, they are
          redirected to the "index" page with an informational message.
        - If the user is not authenticated, they are redirected to the "login_usuario"
          page with a warning message.

    Example:
        @session_rol_permission("admin", "editor")
        def my_view(request):
            # View logic here
            pass
    """
    def decorador(func):
        def decorada(request, *args, **kwargs):
            autenticado = request.session.get("pista", False)
            if autenticado:
                if len(roles) == 0 or (autenticado["rol"] in roles):
                    return func(request, *args, **kwargs)
                else:
                    messages.info(request, "Usted no está autorizado")
                    return redirect("index")
            else:
                messages.warning(request, "Usted no ha iniciado sesión")
                return redirect("login_usuario")
        return decorada
    return decorador
