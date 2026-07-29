from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import categorias, ordenes, mesas, productos, usuarios, detallesOrdenes, comentarios
from .utils.bd_mongo import logs_colletion, normalizar_para_mongo
from .utils.utils import tomar_cliente_ip, get_request_actual
from datetime import datetime
CAMPOS_SENSIBLES = {'password', '_state', 'last_login'}

_estado_anterior = {}

def _obtener_estado_anterior(instance):
    key = f"{instance.__class__.__name__}_{instance.pk}"
    return _estado_anterior.pop(key, None)

def _guardar_estado_anterior(instance):
    try:
        old = instance.__class__._default_manager.get(pk=instance.pk)
        key = f"{instance.__class__.__name__}_{instance.pk}"
        _estado_anterior[key] = old
    except instance.__class__.DoesNotExist:
        pass

def _calcular_cambios(old_instance, new_instance):
    if old_instance is None:
        return None
    cambios = {}
    old_dict = old_instance.__dict__
    new_dict = new_instance.__dict__
    todos_los_campos = set(list(old_dict.keys()) + list(new_dict.keys()))
    for campo in todos_los_campos:
        if campo in CAMPOS_SENSIBLES:
            continue
        old_val = old_dict.get(campo)
        new_val = new_dict.get(campo)
        if str(old_val) != str(new_val):
            cambios[campo] = {'antes': normalizar_para_mongo(old_val), 'despues': normalizar_para_mongo(new_val)}
    return cambios if cambios else None

def registrar_en_mongo(sender, instance, accion, request=None):
    try:
        ip = tomar_cliente_ip(request)
        usuario = 'Sistema'
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            usuario = str(request.user)

        data_normalizada = {
            k: v for k, v in instance.__dict__.items()
            if k not in CAMPOS_SENSIBLES
        }
        data_normalizada = normalizar_para_mongo(data_normalizada)

        log_date = {
            'modelo': sender.__name__,
            'id_objeto': str(instance.pk),
            'accion': accion,
            'usuario': usuario,
            'ip': ip,
            'fecha': datetime.now(),
            'data': data_normalizada,
        }

        if accion == "ACTUALIZADO":
            old_instance = _obtener_estado_anterior(instance)
            cambios = _calcular_cambios(old_instance, instance)
            if cambios:
                log_date['cambios'] = cambios

        logs_colletion.insert_one(log_date)
    except Exception:
        pass

@receiver(pre_save, sender=categorias)
def pre_categorias(sender, instance, **kwargs):
    if instance.pk:
        _guardar_estado_anterior(instance)

@receiver(post_save, sender=categorias)
def auditar_categorias_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    request = get_request_actual()
    registrar_en_mongo(sender, instance, accion, request=request)
@receiver(post_delete, sender=categorias)
def auditar_categorias_delete(sender, instance, **kwargs):
    request = get_request_actual()
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(pre_save, sender=ordenes)
def pre_ordenes(sender, instance, **kwargs):
    if instance.pk:
        _guardar_estado_anterior(instance)

@receiver(post_save, sender=ordenes)
def auditar_ordenes_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    request = get_request_actual()
    registrar_en_mongo(sender, instance, accion, request=request)
@receiver(post_delete, sender=ordenes)
def auditar_ordenes_delete(sender, instance, **kwargs):
    request = get_request_actual()
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(pre_save, sender=mesas)
def pre_mesas(sender, instance, **kwargs):
    if instance.pk:
        _guardar_estado_anterior(instance)

@receiver(post_save, sender=mesas)
def auditar_mesas_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    request = get_request_actual()
    registrar_en_mongo(sender, instance, accion, request=request)
@receiver(post_delete, sender=mesas)
def auditar_mesas_delete(sender, instance, **kwargs):
    request = get_request_actual()
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(pre_save, sender=productos)
def pre_productos(sender, instance, **kwargs):
    if instance.pk:
        _guardar_estado_anterior(instance)

@receiver(post_save, sender=productos)
def auditar_productos_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    request = get_request_actual()
    registrar_en_mongo(sender, instance, accion, request=request)
@receiver(post_delete, sender=productos)
def auditar_productos_delete(sender, instance, **kwargs):
    request = get_request_actual()
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(pre_save, sender=usuarios)
def pre_usuarios(sender, instance, **kwargs):
    if instance.pk:
        _guardar_estado_anterior(instance)

@receiver(post_save, sender=usuarios)
def auditar_usuarios_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    request = get_request_actual()
    registrar_en_mongo(sender, instance, accion, request=request)
@receiver(post_delete, sender=usuarios)
def auditar_usuarios_delete(sender, instance, **kwargs):
    request = get_request_actual()
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(pre_save, sender=detallesOrdenes)
def pre_detallesOrdenes(sender, instance, **kwargs):
    if instance.pk:
        _guardar_estado_anterior(instance)

@receiver(post_save, sender=detallesOrdenes)
def auditar_detallesOrdenes_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    request = get_request_actual()
    registrar_en_mongo(sender, instance, accion, request=request)
@receiver(post_delete, sender=detallesOrdenes)
def auditar_detallesOrdenes_delete(sender, instance, **kwargs):
    request = get_request_actual()
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(pre_save, sender=comentarios)
def pre_comentarios(sender, instance, **kwargs):
    if instance.pk:
        _guardar_estado_anterior(instance)

@receiver(post_save, sender=comentarios)
def auditar_comentarios_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    request = get_request_actual()
    registrar_en_mongo(sender, instance, accion, request=request)
@receiver(post_delete, sender=comentarios)
def auditar_comentarios_delete(sender, instance, **kwargs):
    request = get_request_actual()
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)


from django.db.models import Sum
def actualizar_monto_total_orden(orden):
    # Sumamos todos los subtotales de los detalles relacionados a esta orden
    resultado = orden.detalles.aggregate(total=Sum('subtotal'))
    monto_calculado = resultado['total'] or 0.00
    ordenes.objects.filter(pk=orden.pk).update(monto_total=monto_calculado)

@receiver(post_save, sender=detallesOrdenes)
def actualizar_total_al_guardar_detalle(sender, instance, **kwargs):
    actualizar_monto_total_orden(instance.orden_fk)

@receiver(post_delete, sender=detallesOrdenes)
def actualizar_total_al_eliminar_detalle(sender, instance, **kwargs):
    actualizar_monto_total_orden(instance.orden_fk)