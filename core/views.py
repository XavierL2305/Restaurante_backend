from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

import logging
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets

from .models import usuarios, mesas, categorias, productos, ordenes, detallesOrdenes, comentarios, favoritos
from .serializers import (
    UsuariosSerializado,
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
        # 1. Contamos las órdenes (Filtramos por pagadas para no contar las canceladas o pendientes)
        pedidos_count = ordenes.objects.filter(
            cliente_id=user_id, 
            estatus='pagado' # Solo las que sí se concluyeron
        ).count()

        # 2. Contamos las reseñas/comentarios (Solo los activos)
        resenas_count = comentarios.objects.filter(
            usuario_fk_id=user_id, 
            estatus=True
        ).count()

        # 3. Contamos los favoritos 
        # NOTA: Como aún no creas el modelo de favoritos en tu BD, lo dejamos en 0 temporalmente
        favoritos_count = favoritos.objects.filter(
            usuario_fk_id=user_id,
        ).count()

        # 4. Devolvemos el JSON con los números exactos que espera tu frontend
        return Response({
            'pedidos': pedidos_count,
            'favoritos': favoritos_count,
            'reseñas': resenas_count
        })

class UsuariosVistaSet(viewsets.ModelViewSet):
    queryset = usuarios.objects.all()
    serializer_class = UsuariosSerializado
    permission_classes = [IsAuthenticatedOrReadOnly]

class MesasVistaSet(viewsets.ModelViewSet):
    queryset = mesas.objects.all()
    serializer_class = MesasSerializado
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoriasVistaSet(viewsets.ModelViewSet):
    queryset = categorias.objects.all()
    serializer_class = CategoriasSerializado
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductosVistaSet(viewsets.ModelViewSet):
    queryset = productos.objects.all()
    serializer_class = ProductosSerializado
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_fk_id = self.request.query_params.get('categoria_fk')
        if categoria_fk_id:
            queryset = queryset.filter(categoria_fk_id=categoria_fk_id)
        return queryset
    
from rest_framework.filters import SearchFilter

class OrdenesVistaSet(viewsets.ModelViewSet):
    queryset = ordenes.objects.all()
    serializer_class = OrdenesSerializado
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        orden_fk_id = self.request.query_params.get('orden_fk')
        if orden_fk_id:
            queryset = queryset.filter(orden_fk_id = orden_fk_id)
        return queryset

class ComentariosVistaSet(viewsets.ModelViewSet):
    queryset = comentarios.objects.all()
    serializer_class = ComentariosSerializado
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        usuario_fk_id = self.request.query_params.get('usuario_fk')
        if usuario_fk_id:
            queryset = queryset.filter(usuario_fk_id = usuario_fk_id)
        
        producto_fk_id = self.request.query_params.get('producto_fk')
        if producto_fk_id:
            queryset = queryset.filter(producto_fk_id = producto_fk_id)
        return queryset

class RegistroUsuarioVistaSet(generics.CreateAPIView):
    queryset = usuarios.objects.all()
    serializer_class = UsuariosSerializado
    permission_classes = []

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