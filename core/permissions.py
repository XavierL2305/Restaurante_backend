from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Solo el admin puede crear, editar o borrar.
    Cualquiera puede leer (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsStaffOrAdmin(BasePermission):
    """
    Mesero, cajero o admin pueden escribir.
    Cualquiera autenticado puede leer.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('mesero', 'cajero', 'admin')
        )


class IsOwnerOrStaffOrAdmin(BasePermission):
    """
    - Cliente: solo ve/edita sus propias órdenes.
    - Mesero/Cajero: ven y editan órdenes activas.
    - Admin: acceso total.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role in ('mesero', 'cajero'):
            return True
        if request.user.role == 'cliente':
            return obj.cliente_id == request.user.id
        return False


class IsAuthenticatedForWrite(BasePermission):
    """
    Lectura: cualquiera.
    Escritura: solo autenticado.
    Borrado: solo admin.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return (
                request.user
                and request.user.is_authenticated
                and request.user.role == 'admin'
            )
        return request.user and request.user.is_authenticated


class OrderPermission(BasePermission):
    """
    Permisos específicos para órdenes:
    - Admin: acceso total.
    - Mesero/Cajero: pueden gestionar órdenes (leer, editar, actualizar estado).
    - Cliente: puede crear órdenes, ver las suyas, y cancelar solo las pendientes.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role in ('admin', 'mesero', 'cajero'):
            return True
        if request.user.role == 'cliente':
            if request.method in SAFE_METHODS:
                return True
            if request.method == 'POST':
                return True
            if request.method in ('PUT', 'PATCH', 'DELETE'):
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role in ('mesero', 'cajero'):
            return True
        if request.user.role == 'cliente':
            if obj.cliente_id != request.user.id:
                return False
            if request.method in ('PUT', 'PATCH'):
                return obj.estatus == 'pidiendo'
            if request.method == 'DELETE':
                return obj.estatus == 'pidiendo'
            return True
        return False


class OrderDetailPermission(BasePermission):
    """
    - Admin/Mesero/Cajero: acceso total.
    - Cliente: puede leer sus propios detalles y crear nuevos (para sus órdenes).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role in ('admin', 'mesero', 'cajero'):
            return True
        if request.user.role == 'cliente':
            if request.method in SAFE_METHODS:
                return True
            if request.method == 'POST':
                return True
            return False
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role in ('admin', 'mesero', 'cajero'):
            return True
        if request.user.role == 'cliente':
            return obj.orden_fk.cliente_id == request.user.id
        return False


class IsOwnerOrAdmin(BasePermission):
    """
    El dueño del recurso o un admin pueden acceder.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if hasattr(obj, 'usuario_fk'):
            return obj.usuario_fk_id == request.user.id
        if hasattr(obj, 'cliente'):
            return obj.cliente_id == request.user.id
        return False
