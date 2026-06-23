from rest_framework import serializers
from .models import Usuarios, Mesas, Ordenes, Productos, Categorias

class UsuariosSerializado(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

class MesasSerializado(serializers.ModelSerializer):
    class Meta:
        model = Mesas
        fields = '__all__'

class OrdenesSerializado(serializers.ModelSerializer):
    class Meta:
        model = Ordenes
        fields = '__all__'

class ProductosSerializado(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'

class CategoriasSerializado(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'
