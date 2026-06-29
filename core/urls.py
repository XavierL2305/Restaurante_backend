from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuariosVistaSet,
    MesasVistaSet,
    CategoriasVistaSet,
    ProductosVistaSet,
    OrdenesVistaSet,
    DetallesVistaSet,
    ComentariosVistaSet
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
    path('', include(router.urls))
]