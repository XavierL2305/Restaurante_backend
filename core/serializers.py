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
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    
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

class OrdenesSerializado(serializers.ModelSerializer):
    # --- CAMPOS DE LECTURA ---
    mesa_info = MesasSerializado(source='mesa_fk', read_only=True)
    mesero_info = MeseroCortoSerializado(source='mesero', read_only=True)
    cliente_info = ClienteCortoSerializado(source='cliente', read_only=True)

    mesa_fk = serializers.PrimaryKeyRelatedField(queryset=mesas.objects.all())
    mesero = serializers.PrimaryKeyRelatedField(queryset=usuarios.objects.all(), required=False, allow_null=True)
    cliente = serializers.PrimaryKeyRelatedField(queryset=usuarios.objects.all())

    class Meta:
        model = ordenes
        fields = [
            'id', 'estatus', 'fecha_creacion', 'monto_total', 
            'mesa_fk', 'mesero', 'cliente', 
            'mesa_info', 'mesero_info', 'cliente_info'
        ]
    def create(self, validated_data):
        mesa_instancia = validated_data.pop('mesa_fk', None)
        mesero_instancia = validated_data.pop('mesero', None)
        cliente_instancia = validated_data.pop('cliente', None)

        if mesa_instancia and mesa_instancia.estatus == 'disponible':
            mesa_instancia.estatus = 'ocupado'
            mesa_instancia.save()

        orden = ordenes.objects.create(
            mesa_fk=mesa_instancia,
            mesero=mesero_instancia,
            cliente=cliente_instancia,
            **validated_data
        )
        return orden
    def update(self, instance, validated_data):
        # En el update sí sacamos los IDs (strings) y los buscamos, porque el PATCH viene plano desde el frontend
        mesa_id = validated_data.pop('mesa_fk', None)
        mesero_id = validated_data.pop('mesero', None)
        cliente_id = validated_data.pop('cliente', None)

        if mesa_id:
            instance.mesa_fk = mesas.objects.get(id=mesa_id)
        if mesero_id:
            instance.mesero = usuarios.objects.get(id=mesero_id)
        if cliente_id:
            instance.cliente = usuarios.objects.get(id=cliente_id)

        instance = super().update(instance, validated_data)

        if instance.estatus in ('eliminado', 'pagado'):
            instance.mesa_fk.estatus = 'disponible'
            instance.mesa_fk.save()

        return instance
    
class DetallesSerializado(serializers.ModelSerializer):
    # ✅ OBLIGAMOS A DRF A SER ESTRICTOS CON LOS UUIDS
    producto_fk = serializers.PrimaryKeyRelatedField(queryset=productos.objects.all())
    orden_fk = serializers.PrimaryKeyRelatedField(queryset=ordenes.objects.all())
    
    class Meta:
        model = detallesOrdenes
        fields = '__all__'
        extra_kwargs = {
            'subtotal': {'read_only': True},
        }

class ProductosSerializado(serializers.ModelSerializer):
    class Meta:
        model = productos
        fields = '__all__'

class CategoriasSerializado(serializers.ModelSerializer):
    class Meta:
        model = categorias
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