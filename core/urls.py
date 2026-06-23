from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuariosVistaSet,
    MesasVistaSet,
    CategoriasVistaSet,
    ProductosVistaSet,
    OrdenesVistaSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuariosVistaSet)
router.register(r'mesas', MesasVistaSet)
router.register(r'categorias', CategoriasVistaSet)
router.register(r'productos', ProductosVistaSet)
router.register(r'ordenes', OrdenesVistaSet)

urlpatterns = [
    path('', include(router.urls))
]