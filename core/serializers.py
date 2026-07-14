from rest_framework import serializers
from .models import usuarios, mesas, ordenes, productos, categorias, detallesOrdenes, comentarios
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UsuariosSerializado(serializers.ModelSerializer):
    class Meta:
        model = usuarios
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'role',
            'imagen',
            'is_active'
        ]
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = usuarios(**validated_data)
        if password is not None:
            usuario.set_password(password)
        usuario.save()
        return usuario
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)

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

class DetallesSerializado(serializers.ModelSerializer):
    class Meta:
        model = detallesOrdenes
        fields = '__all__'

class ComentariosSerializado(serializers.ModelSerializer):
    class Meta:
        model = comentarios
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    #Este es un serializador para permitir el inicio de sesion con username o con email
    def validate(self, attrs):
        identificador = attrs.get('username')
        password = attrs.get('password')

        if identificador and password:
            user = authenticate(request=self.context.get('request'), username=identificador, password=password)

            if user is None:
                try:
                    user_obj = usuarios.objects.get(email=identificador)
                    user = authenticate(request=self.context.get('request'), username=user_obj.username, password=password)
                except usuarios.DoesNotExist:
                    pass
            if user is not None and not user.is_active:
                raise serializers.ValidationError(
                    'Tu cuenta ha sido desactivada. Contacta al administrador.',
                    code='authorization'
                )
            if user is None:
                raise serializers.ValidationError(
                    _('Usuario inexistente o credenciales erronias'),code='authorization'
                )
        attrs['username'] = user.username

        return super().validate(attrs)