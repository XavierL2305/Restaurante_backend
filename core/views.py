import json
import logging
from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response

from .models import Usuarios, Mesas, Categorias, Productos, Ordenes
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
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializado

class MesasVistaSet(viewsets.ModelViewSet):
    queryset = Mesas.objects.all()
    serializer_class = MesasSerializado

    # def _registrar_log(self, datos_antes, instance_despues, accion):
    #     campos = instance_despues._meta.fields
    #     datos_despues = {
    #         field.name: getattr(instance_despues, field.name)
    #         for field in campos
    #     }

    #     cambios = {
    #         'antes': datos_antes,
    #         'despues': datos_despues,
    #     }

    #     log_data = {
    #         'modelo': 'Mesas',
    #         'id_objeto': str(instance_despues.pk),
    #         'accion': accion,
    #         'usuario': self.request.user.username if self.request.user.is_authenticated else 'Anonimo',
    #         'fecha': datetime.now(),
    #         'cambios': cambios,
    #         'url': self.request.path,
    #     }

    #     try:
    #         logs_colletion.insert_one(normalizar_para_mongo(log_data))
    #     except Exception:
    #         logger.exception('No se pudo guardar el log en MongoDB')

    # def _normalizar_request(self, request):
    #     if isinstance(request, DRFRequest):
    #         return request
    #     return DRFRequest(request)

    # def _obtener_payload(self, request):
    #     request = self._normalizar_request(request)
    #     try:
    #         payload = getattr(request, 'data', None)
    #         if payload is not None and not isinstance(payload, (dict, list)):
    #             payload = dict(payload)
    #         if payload is not None:
    #             return payload
    #     except Exception:
    #         payload = None

    #     try:
    #         if getattr(request, 'POST', None) is not None:
    #             return request.POST
    #     except Exception:
    #         pass

    #     body = getattr(request, 'body', b'') or b''
    #     if isinstance(body, bytes):
    #         body_text = body.decode('utf-8', errors='ignore').strip()
    #         if body_text:
    #             try:
    #                 return json.loads(body_text)
    #             except json.JSONDecodeError:
    #                 return {}
    #     return {}

    # def _obtener_instancia_existente(self, request):
    #     payload = self._obtener_payload(request)
    #     if not payload:
    #         return None

    #     identificador = self.kwargs.get('pk')
    #     if not identificador:
    #         identificador = payload.get('id') or payload.get('pk') or payload.get('uuid')

    #     if identificador:
    #         try:
    #             return self.get_queryset().get(pk=identificador)
    #         except (Mesas.DoesNotExist, ValueError, TypeError):
    #             pass

    #     if payload.get('numero_mesa') is not None:
    #         try:
    #             return self.get_queryset().get(numero_mesa=payload.get('numero_mesa'))
    #         except Mesas.DoesNotExist:
    #             return None

    #     return None

    # def create(self, request, *args, **kwargs):
    #     request = self._normalizar_request(request)
    #     self.request = request
    #     payload = self._obtener_payload(request)
    #     instancia_existente = self._obtener_instancia_existente(request)
    #     if instancia_existente is not None:
    #         serializer = self.get_serializer(instancia_existente, data=payload, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     return super().create(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     request = self._normalizar_request(request)
    #     self.request = request
    #     payload = self._obtener_payload(request)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=payload)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # def partial_update(self, request, *args, **kwargs):
    #     request = self._normalizar_request(request)
    #     self.request = request
    #     payload = self._obtener_payload(request)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=payload, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     instance_despues = serializer.save()
    #     self._registrar_log({}, instance_despues, 'CREATE')

    # def perform_update(self, serializer):
    #     instance_antes = serializer.instance
    #     datos_antes = {
    #         field.name: getattr(instance_antes, field.name)
    #         for field in instance_antes._meta.fields
    #     }
    #     instance_despues = serializer.save()
    #     self._registrar_log(datos_antes, instance_despues, 'UPDATE')

class CategoriasVistaSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializado

class ProductosVistaSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializado

class OrdenesVistaSet(viewsets.ModelViewSet):
    queryset = Ordenes.objects.all()
    serializer_class = OrdenesSerializado