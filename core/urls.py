from django.urls import path, include
from .google_auth import GoogleLoginView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    UsuariosVistaSet,
    MesasVistaSet,
    CategoriasVistaSet,
    ProductosVistaSet,
    OrdenesVistaSet,
    DetallesVistaSet,
    ComentariosVistaSet,

    RegistroUsuarioVistaSet,
    LoginUsuarioVistaSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuariosVistaSet)
router.register(r'mesas', MesasVistaSet)
router.register(r'categorias', CategoriasVistaSet)
router.register(r'productos', ProductosVistaSet)
router.register(r'ordenes', OrdenesVistaSet)
router.register(r'detalles', DetallesVistaSet)
router.register(r'comentarios', ComentariosVistaSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/login/', LoginUsuarioVistaSet.as_view(), name='auth_login'),
    path('auth/registro/', RegistroUsuarioVistaSet.as_view(), name='auth_register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]