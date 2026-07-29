from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from decouple import config

import logging
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly, IsStaffOrAdmin, IsOwnerOrStaffOrAdmin, IsAuthenticatedForWrite, IsOwnerOrAdmin, OrderPermission, OrderDetailPermission, UserProfilePermission
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import usuarios, mesas, categorias, productos, ordenes, detallesOrdenes, comentarios, favoritos
from .serializers import (
    UsuariosSerializado,
    RegistroUsuariosSerializado,
    MesasSerializado,
    CategoriasSerializado,
    ProductosSerializado,
    OrdenesSerializado,
    DetallesSerializado,
    ComentariosSerializado,
    favoritosSerializado,

    CustomTokenObtainPairSerializer
)
# from .utils.bd_mongo import logs_colletion, normalizar_para_mongo

logger = logging.getLogger(__name__)

# Create your views here.

class UsuarioStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        if user.role == 'cliente' and str(user.id) != str(user_id):
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        pedidos_count = ordenes.objects.filter(
            cliente_id=user_id, 
            estatus='pagado'
        ).count()

        resenas_count = comentarios.objects.filter(
            usuario_fk_id=user_id, 
            estatus=True
        ).count()

        favoritos_count = favoritos.objects.filter(
            usuario_fk_id=user_id,
        ).count()

        return Response({
            'pedidos': pedidos_count,
            'favoritos': favoritos_count,
            'reseñas': resenas_count
        })

class UsuariosVistaSet(viewsets.ModelViewSet):
    queryset = usuarios.objects.all()
    serializer_class = UsuariosSerializado
    permission_classes = [UserProfilePermission]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

class MesasVistaSet(viewsets.ModelViewSet):
    queryset = mesas.objects.all()
    serializer_class = MesasSerializado
    permission_classes = [IsAdminOrReadOnly]

class CategoriasVistaSet(viewsets.ModelViewSet):
    queryset = categorias.objects.all()
    serializer_class = CategoriasSerializado
    permission_classes = [IsAdminOrReadOnly]

class ProductosVistaSet(viewsets.ModelViewSet):
    queryset = productos.objects.all()
    serializer_class = ProductosSerializado
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        categoria_fk_id = self.request.query_params.get('categoria_fk')
        if categoria_fk_id:
            queryset = queryset.filter(categoria_fk_id=categoria_fk_id)
        return queryset

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminOrReadOnly])
    def restaurar(self, request, pk=None):
        producto = self.get_object()
        producto.restaurar()
        serializer = self.get_serializer(producto)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrReadOnly])
    def inactivos(self, request):
        queryset = productos.objects.filter(estatus=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
from rest_framework.filters import SearchFilter

class OrdenesVistaSet(viewsets.ModelViewSet):
    queryset = ordenes.objects.all()
    serializer_class = OrdenesSerializado
    permission_classes = [OrderPermission]
    filter_backends = [SearchFilter]
    search_fields = ['cliente__first_name', 'cliente__email', 'mesa_fk__numero_mesa']
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user  # <-- Django obtiene el usuario del token automáticamente

        # 1. Si es un cliente autenticado, FORZAMOS a que solo vea sus propias órdenes
        if user.is_authenticated and user.role == 'cliente':
            return queryset.filter(cliente_id=user.id)

        # 2. Si es ADMIN, MESERO o CAJERO, aplicamos los filtros normales de la URL:
        mesero_id = self.request.query_params.get('mesero')
        if mesero_id:
            queryset = queryset.filter(mesero_id=mesero_id)
        
        cliente_id = self.request.query_params.get('cliente')
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        mesa_fk_id = self.request.query_params.get('mesa_fk')
        if mesa_fk_id:
            queryset = queryset.filter(mesa_fk_id=mesa_fk_id)
        
        estatus = self.request.query_params.get('estatus')
        if estatus:
            queryset = queryset.filter(estatus=estatus) # Asegúrate de que tu modelo tenga el campo 'estatus' escrito igual
        return queryset

class DetallesVistaSet(viewsets.ModelViewSet):
    queryset = detallesOrdenes.objects.all()
    serializer_class = DetallesSerializado
    permission_classes = [OrderDetailPermission]
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role == 'cliente':
            queryset = queryset.filter(orden_fk__cliente_id=user.id)
        orden_fk_id = self.request.query_params.get('orden_fk')
        if orden_fk_id:
            queryset = queryset.filter(orden_fk_id=orden_fk_id)
        return queryset

class ComentariosVistaSet(viewsets.ModelViewSet):
    queryset = comentarios.objects.all()
    serializer_class = ComentariosSerializado
    permission_classes = [IsOwnerOrAdmin]
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role == 'cliente':
            return queryset.filter(usuario_fk_id=user.id)
        usuario_fk_id = self.request.query_params.get('usuario_fk')
        if usuario_fk_id:
            queryset = queryset.filter(usuario_fk_id = usuario_fk_id)
        
        producto_fk_id = self.request.query_params.get('producto_fk')
        if producto_fk_id:
            queryset = queryset.filter(producto_fk_id = producto_fk_id)
        return queryset

class FavoritosVistaSet(viewsets.ModelViewSet):
    queryset = favoritos.objects.all()
    serializer_class = favoritosSerializado
    permission_classes = [IsOwnerOrAdmin]
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role == 'cliente':
            return queryset.filter(usuario_fk_id=user.id)
        usuario_fk_id = self.request.query_params.get('usuario_fk')
        if usuario_fk_id:
            queryset = queryset.filter(usuario_fk_id = usuario_fk_id)
        
        producto_fk_id = self.request.query_params.get('producto_fk')
        if producto_fk_id:
            queryset = queryset.filter(producto_fk_id = producto_fk_id)
        return queryset

class RegistroUsuarioVistaSet(generics.CreateAPIView):
    queryset = usuarios.objects.all()
    serializer_class = RegistroUsuariosSerializado
    permission_classes = []
    throttle_scope = 'registration'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Token >>>>
        refresh = RefreshToken.for_user(user)

        return Response({
            'message':'Usuario creado exitosamente',
            'access':str(refresh.access_token),
            'refresh':str(refresh),
            'user':{
                'id':str(user.id),
                'email':user.email,
                'first_name':user.first_name,
                'role':user.role
            }
        }, status=status.HTTP_201_CREATED)
class LoginUsuarioVistaSet(TokenObtainPairView):
    permission_classes = []
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            tokens = response.data

            decoded_token = AccessToken(tokens['access'])
            user_id = decoded_token['user_id']

            user = usuarios.objects.get(id=user_id)

            return Response({
                'message': 'Login exitoso',
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'first_name': user.first_name,
                    'role': user.role
                }
            }, status=status.HTTP_200_OK)
        return response


class AuditoriaVista(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        from .utils.bd_mongo import logs_colletion
        from bson import json_util
        import json

        modelo = request.query_params.get('modelo')
        accion = request.query_params.get('accion')
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        buscar = request.query_params.get('buscar')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        query = {}
        if modelo:
            query['modelo'] = modelo
        if accion:
            query['accion'] = accion
        if fecha_desde or fecha_hasta:
            fecha_query = {}
            if fecha_desde:
                fecha_query['$gte'] = fecha_desde
            if fecha_hasta:
                fecha_query['$lte'] = fecha_hasta + 'T23:59:59'
            query['fecha'] = fecha_query
        if buscar:
            query['$or'] = [
                {'usuario': {'$regex': buscar, '$options': 'i'}},
                {'id_objeto': {'$regex': buscar, '$options': 'i'}},
                {'ip': {'$regex': buscar, '$options': 'i'}},
            ]

        total = logs_colletion.count_documents(query)
        skip = (page - 1) * page_size
        logs = list(
            logs_colletion.find(query)
            .sort('fecha', -1)
            .skip(skip)
            .limit(page_size)
        )

        logs_serializados = []
        for log in logs:
            log['_id'] = str(log['_id'])
            if 'fecha' in log:
                log['fecha'] = log['fecha'].isoformat()
            logs_serializados.append(log)

        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size,
            'results': logs_serializados,
        })
class PasswordResetView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email', '').strip()
        new_password = request.data.get('new_password', '').strip()

        if not email:
            return Response({'error': 'El correo es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = usuarios.objects.get(email=email, is_active=True)
        except usuarios.DoesNotExist:
            return Response(
                {'detail': 'Si el correo está registrado, podrás restablecer tu contraseña.'},
                status=status.HTTP_200_OK
            )

        if not new_password:
            return Response({'email_exists': True, 'detail': 'Correo verificado'}, status=status.HTTP_200_OK)

        if len(new_password) < 8:
            return Response({'error': 'La contraseña debe tener al menos 8 caracteres'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Contraseña actualizada exitosamente'}, status=status.HTTP_200_OK)

# Para tomar los estatus y usarlos en el frontend

ESTATUS_COLORES = {
    'eliminado': '#BDBDBD',
    'pidiendo': '#FF9800',
    'cocinando': '#F44336',
    'finalizado': '#2196F3',
    'delivery': '#9C27B0',
    'pagado': '#4CAF50',
}

class EstatusOrdenVista(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        estatus = [
            {
                'value': choice[0],
                'label': choice[1],
                'color': ESTATUS_COLORES.get(choice[0], '#EFEFEF'),
            }
            for choice in ordenes.ESTATUS_CHOICES
        ]
        return Response(estatus)
