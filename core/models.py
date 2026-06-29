from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.

class usuarios(AbstractUser):
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
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')
    imagen = models.ImageField(upload_to='usuarios_media', null=True, blank=True)
    objects = models.Manager()
    activos = models.Manager()
    class Meta:
        db_table = 'usuarios'
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
    def restaurar(self):
        self.is_active = True
        self.save()
    def __str__(self):
        return f"Usuario {str(self.id)[:8]}:{self.first_name} {self.last_name}"

class mesas(models.Model):
    ESTATUS_CHOICES = [
        ('eliminado','Eliminado'),
        ('disponible','Disponible'),
        ('ocupado','Ocupado')
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    numero_mesa = models.IntegerField()
    estatus = models.CharField(max_length=20, choices = ESTATUS_CHOICES, default='disponible')
    objects = models.Manager()
    activos = models.Manager()
    class Meta:
        db_table = 'mesas'
    def delete(self, *args, **kwargs):
        self.estatus = 'eliminado'
        self.save()
    def restaurar(self):
        self.estatus = 'disponible'
        self.save()
    def __str__(self):
        return f"Mesa {str(self.id)[:8]}:{self.numero_mesa}"

class categorias(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre = models.CharField(max_length=100)
    estatus = models.BooleanField(default=True)
    objects = models.Manager()
    activos = models.Manager()
    class Meta:
        db_table = 'categorias'
    def delete(self, *args, **kwargs):
        self.estatus = False
        self.save()
    def restaurar(self):
        self.estatus = True
        self.save()
    def __str__(self):
        return f"Categoria {str(self.id)[:8]}:{self.nombre}"

class productos(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria_fk = models.ForeignKey(categorias, on_delete=models.CASCADE)
    estatus = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos_media/', null=True, blank=True)
    objects = models.Manager()
    activos = models.Manager()
    class Meta:
        db_table = 'productos'
    def delete(self, *args, **kwargs):
        self.estatus = False
        self.save()
    def restaurar(self):
        self.estatus = True
        self.save()
    def __str__(self):
        return f"Producto {self.id}...- Categoria {str(self.categoria_fk.id)[:8]}:{str(self.categoria_fk.nombre)}"

class ordenes(models.Model):
    ESTATUS_CHOICES = [
        ('eliminado','Eliminado'),
        ('hablitado','Habilitado'),
        ('pidiendo', 'Pidiendo'),
        ('cocinando', 'Cocinando'),
        ('finalizado', 'Finalizado'),
        ('delivery', 'Delivery'),
        ('entregado', 'Entregado'),
        ('pagado', 'Pagado')
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='pidiendo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    mesa_fk = models.ForeignKey(mesas, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mesero =models.ForeignKey(
        usuarios,
        on_delete=models.CASCADE, # Cambiar a models.PROTECTED luego de culminar las pruebas de construccion
        related_name='ordenes_asignadas',
        limit_choices_to={'role':'mesero'},
    )
    cliente = models.ForeignKey(
        usuarios,
        on_delete=models.CASCADE, # Cambiar a models.PROTECTED luego de culminar las pruebas de construccion
        related_name='mis_ordenes',
        limit_choices_to={'role':'cliente'}
    )
    objects = models.Manager()
    activos = models.Manager()
    class Meta:
        db_table = 'ordenes'
        ordering = ['-fecha_creacion']
    def delete(self, *args, **kwargs):
        self.estatus = 'eliminado'
        self.save()
    def restaurar(self):
        self.estatus = 'habilitado'
        self.save()
    def __str__(self):
        return f"Orden {str(self.id)[:8]}... - Mesa {str(self.mesa_fk.id)[:8]}: {str(self.mesa_fk)}... - Mesero {str(self.mesero.id)[:8]}: {self.mesero.first_name} {self.mesero.last_name}... - Cliente {str(self.cliente.id)[:8]}: {self.cliente.first_name} {self.cliente.last_name}"

class detallesOrdenes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto_fk = models.ForeignKey(
        productos, 
        on_delete=models.CASCADE, # Cambiar a models.PROTECTED luego de culminar las pruebas de construccion
        related_name='detalles_en_ordenes'
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estatus = models.BooleanField(default=True)
    orden_fk = models.ForeignKey(ordenes, on_delete=models.CASCADE, related_name='detalles')
    objects = models.Manager()
    activos = models.Manager()
    class Meta:
        db_table = 'detalles_ordenes'
    def delete(self, *args, **kwargs):
        self.estatus = False
        self.save()
    def restaurar(self):
        self.estatus = True
        self.save()
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio
        super().save(*args, **kwargs)
        total_actualizado = sum(detalle.subtotal for detalle in self.orden_fk.detalles.filter(estatus = True))
        
        self.orden_fk.monto_total = total_actualizado
        self.orden_fk.save()
    def __str__(self):
        return f"{self.cantidad} x {self.precio}... - Orden: {str(self.orden_fk.id)[:8]}"

class comentarios(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descripcion = models.TextField(max_length=200)
    likes = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='comentarios_media/', blank=True, null=True)
    estatus = models.BooleanField(default=True)
    usuario_fk = models.ForeignKey(
        usuarios, 
        on_delete=models.CASCADE # Cambiar a models.PROTECTED luego de culminar las pruebas de construccion
    )
    producto_fk = models.ForeignKey(
        productos, 
        on_delete=models.CASCADE # Cambiar a models.PROTECTED luego de culminar las pruebas de construccion
    )
    objects = models.Manager()
    activos = models.Manager()
    class Meta:
        db_table = 'comentarios'
    def delete(self, *args, **kwargs):
        self.estatus = False
        self.save()
    def restaurar(self):
        self.estatus = True
        self.save()
    def __str__(self):
        return f"Comentario {str(self.id)[:8]}... Usuario {str(self.usuario_fk.id)[:8]}: {self.usuario_fk.username}... - Producto {str(self.producto_fk.id)[:8]}"