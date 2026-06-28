from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import categorias, ordenes, mesas, productos, usuarios, detallesOrdenes, comentarios
from .utils.bd_mongo import logs_colletion
from .utils.utils import tomar_cliente_ip
from datetime import datetime

def registrar_en_mongo(sender, instance, accion, usuario='Sistema', request=None):
    ip = tomar_cliente_ip(request)
    log_date = {
        'modelo': sender.__name__,
        'id_objeto': str(instance.pk),
        'accion': accion,
        'usuario': str(usuario),
        'ip': ip,
        'fecha': datetime.now(),
        'data': f"{instance.__dict__}",
    }
    logs_colletion.insert_one(log_date)

@receiver(post_save, sender=categorias)
def auditar_categorias_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=categorias)
def auditar_categorias_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=ordenes)
def auditar_ordenes_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=ordenes)
def auditar_ordenes_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=mesas)
def auditar_mesas_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=mesas)
def auditar_mesas_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=productos)
def auditar_productos_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=productos)
def auditar_productos_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=usuarios)
def auditar_usuarios_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=usuarios)
def auditar_usuarios_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=detallesOrdenes)
def auditar_detallesOrdenes_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'detalles_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=detallesOrdenes)
def auditar_detallesOrdenes_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=comentarios)
def auditar_comentarios_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'comentarios_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=comentarios)
def auditar_comentarios_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
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