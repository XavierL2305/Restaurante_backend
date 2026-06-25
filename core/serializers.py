from rest_framework import serializers
from .models import usuarios, mesas, ordenes, productos, categorias

class UsuariosSerializado(serializers.ModelSerializer):
    class Meta:
        model = usuarios
        fields = '__all__'

class MesasSerializado(serializers.ModelSerializer):
    class Meta:
        model = mesas
        fields = '__all__'

class OrdenesSerializado(serializers.ModelSerializer):
    class Meta:
        model = ordenes
        fields = '__all__'

class ProductosSerializado(serializers.ModelSerializer):
    class Meta:
        model = productos
        fields = '__all__'

class CategoriasSerializado(serializers.ModelSerializer):
    class Meta:
        model = categorias
        fields = '__all__'
