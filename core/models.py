from django.db import models
from django.core.validators import validate_email
import uuid

# Create your models here.

class usuarios(models.Model):
    ROLE_CHOICES = [
        ('cliente', 'Cliente'), 
        ('mesero', 'Mesero'), 
        ('cajero','Cajero'), 
        ('admin','Admin')
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length = 255, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='usuarios_media', null=True, blank=True)
    def get_old_instance(self):
        return mesas.objects.get(pk=self.pk)
    class Meta:
        db_table = 'usuarios'

class mesas(models.Model):
    ESTATUS_CHOICES = [
        ('disponible','Disponible'),
        ('ocupado','Ocupado')
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    numero_mesa = models.IntegerField()
    estatus = models.CharField(max_length=20, choices = ESTATUS_CHOICES)
    def get_old_instance(self):
        return mesas.objects.get(pk=self.pk)
    class Meta:
        db_table = 'mesas'

class categorias(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre = models.CharField(max_length=100)
    def get_old_instance(self):
        return mesas.objects.get(pk=self.pk)
    class Meta:
        db_table = 'categorias'

class productos(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria_fk = models.ForeignKey(categorias, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos_media/', null=True, blank=True)
    def get_old_instance(self):
        return mesas.objects.get(pk=self.pk)
    class Meta:
        db_table = 'productos'

class ordenes(models.Model):
    ESTATUS_CHOICES = [
        ('pidiendo', 'Pidiendo'),
        ('cocinando', 'Cocinando'),
        ('finalizado', 'Finalizado'),
        ('delivery', 'Delivery'),
        ('entregado', 'Entregado'),
        ('pagado', 'Pagado')
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    mesa_fk = models.ForeignKey(mesas, on_delete=models.CASCADE)
    usuario_fk = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def get_old_instance(self):
        return mesas.objects.get(pk=self.pk)
    class Meta:
        db_table = 'ordenes'