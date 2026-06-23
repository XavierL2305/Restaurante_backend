from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Categorias, Ordenes, Mesas, Productos, Usuarios
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

@receiver(post_save, sender=Categorias)
def auditar_categorias_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=Categorias)
def auditar_categorias_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=Ordenes)
def auditar_ordenes_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=Ordenes)
def auditar_ordenes_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=Mesas)
def auditar_mesas_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=Mesas)
def auditar_mesas_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=Productos)
def auditar_productos_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=Productos)
def auditar_productos_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)

@receiver(post_save, sender=Usuarios)
def auditar_usuarios_save(sender, instance, created, **kwargs):
    accion = "CREADO" if created else "ACTUALIZADO"
    usuario = getattr(instance, 'usuario_modificador', 'Sistema')
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, accion, usuario=usuario, request=request)
@receiver(post_delete, sender=Usuarios)
def auditar_usuarios_delete(sender, instance, **kwargs):
    request = kwargs.get('request')
    registrar_en_mongo(sender, instance, "ELIMINADO", request=request)