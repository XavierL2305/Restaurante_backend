import logging

from rest_framework import viewsets

from .models import usuarios, mesas, categorias, productos, ordenes
from .serializers import (
    UsuariosSerializado,
    MesasSerializado,
    CategoriasSerializado,
    ProductosSerializado,
    OrdenesSerializado,
)
# from .utils.bd_mongo import logs_colletion, normalizar_para_mongo

logger = logging.getLogger(__name__)

# Create your views here.

class UsuariosVistaSet(viewsets.ModelViewSet):
    queryset = usuarios.objects.all()
    serializer_class = UsuariosSerializado

class MesasVistaSet(viewsets.ModelViewSet):
    queryset = mesas.objects.all()
    serializer_class = MesasSerializado

class CategoriasVistaSet(viewsets.ModelViewSet):
    queryset = categorias.objects.all()
    serializer_class = CategoriasSerializado

class ProductosVistaSet(viewsets.ModelViewSet):
    queryset = productos.objects.all()
    serializer_class = ProductosSerializado

class OrdenesVistaSet(viewsets.ModelViewSet):
    queryset = ordenes.objects.all()
    serializer_class = OrdenesSerializado