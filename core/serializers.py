from rest_framework import serializers
from .models import usuarios, mesas, ordenes, productos, categorias, detallesOrdenes, comentarios, favoritos
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

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
    def validate_email(self, value):
        if usuarios.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con ese correo electrónico")
        return value
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

# Serializadores "ligeros" con campos específicos
class MeseroCortoSerializado(serializers.ModelSerializer):
    class Meta:
        model = usuarios  # Ajusta al nombre exacto de tu modelo si cambia
        fields = ('id', 'first_name', 'last_name')

class ClienteCortoSerializado(serializers.ModelSerializer):
    class Meta:
        model = usuarios
        fields = ('id', 'first_name', 'email')

# Ahora los usas en tu serializador de Órdenes
class OrdenesSerializado(serializers.ModelSerializer):
    mesa_fk = MesasSerializado(read_only=True)
    mesero = MeseroCortoSerializado(read_only=True)  # <-- Usamos el corto
    cliente = ClienteCortoSerializado(read_only=True)  # <-- Usamos el corto
    
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

class favoritosSerializado(serializers.ModelSerializer):
    class Meta:
        model = favoritos
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    #Este es un serializador para permitir el inicio de sesion con username o con email
    def validate(self, attrs):
        identificador = attrs.get('username')
        password = attrs.get('password')

        if identificador and password:
            cache_key = f'login_attempts_{identificador}'
            intentos = cache.get(cache_key, 0)

            if intentos >= 3:
                raise serializers.ValidationError(
                    'Demasiados intentos fallidos. Por seguridad, debes esperar 1 minuto antes de intentar nuevamente.',
                    code='authorization'
                )

            user = None
            
            user = authenticate(request=self.context.get('request'), username=identificador, password=password)
            
            if user is None:
                try:
                    user_obj = usuarios.objects.get(email=identificador)
                    user = authenticate(request=self.context.get('request'), username=user_obj.username, password=password)
                except usuarios.DoesNotExist:
                    pass
            if user is None:
                cache.set(cache_key, intentos + 1, 60)
                intentos_restantes = 3 - (intentos + 1)
                mensaje = f'Credenciales incorrectas. Te quedan {intentos_restantes} intento(s).'
                raise serializers.ValidationError(mensaje, code='authorization')

            if not user.is_active:
                raise serializers.ValidationError(
                    'Tu cuenta ha sido desactivada. Contacta al administrador.',
                    code='authorization'
                )

        attrs['username'] = user.username
        return super().validate(attrs)