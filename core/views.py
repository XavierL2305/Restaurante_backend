from rest_framework import viewsets
from .models import Usuarios, Mesas, Categorias, Productos, Ordenes
from .serializers import (
    UsuariosSerializado, 
    MesasSerializado,
    CategoriasSerializado,
    ProductosSerializado,
    OrdenesSerializado
)

# Create your views here.

class UsuariosVistaSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializado

class MesasVistaSet(viewsets.ModelViewSet):
    queryset = Mesas.objects.all()
    serializer_class = MesasSerializado

class CategoriasVistaSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializado

class ProductosVistaSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializado

class OrdenesVistaSet(viewsets.ModelViewSet):
    queryset = Ordenes.objects.all()
    serializer_class = OrdenesSerializado