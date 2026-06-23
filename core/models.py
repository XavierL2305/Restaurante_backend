from django.db import models
import uuid

# Create your models here.

class Usuarios(models.Model):
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
    email = models.CharField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Usuarios'

class Mesas(models.Model):
    ESTATUS_CHOICES = [
        ('disponible','Disponible'),
        ('ocupado','Ocupado')
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    numero_mesa = models.IntegerField()
    estatus = models.CharField(max_length=20, choices = ESTATUS_CHOICES)
    class Meta:
        db_table = 'Mesas'

class Categorias(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre = models.CharField(max_length=100)
    class Meta:
        db_table = 'Categorias'

class Productos(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria_fk = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Productos'

class Ordenes(models.Model):
    ESTATUS_CHOICES = [
        ('pidiendo', 'Pidiendo'),
        ('cocinando', 'Cocinando'),
        ('finalizado', 'Finalizado'),
        ('delivery', 'Delivery'),
        ('entregado', 'Entregado'),
        ('pagado', 'Pagado')
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    mesa_fk = models.ForeignKey(Mesas, on_delete=models.CASCADE)
    usuario_fk = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Ordenes'