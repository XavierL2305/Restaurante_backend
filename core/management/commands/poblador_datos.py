from django.core.management.base import BaseCommand
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from core.models import categorias, productos, mesas, usuarios, comentarios, ordenes, detallesOrdenes, favoritos

class Command(BaseCommand):
    help = 'Poblando la base de datos con datos de prueba'
    detalles = "Aca es donde se detalla el producto (Comida, bebida...)"
    def handle(self, *args, **options):
        self.stdout.write('Borrando datos anteriores')
        usuarios.objects.all().delete()
        categorias.objects.all().delete()
        mesas.objects.all().delete()
        ordenes.objects.all().delete()
        productos.objects.all().delete()
        favoritos.objects.all().delete()

        self.stdout.write('Creando categorías...')
        cat1 = categorias.objects.create(nombre='Platos Fuertes', imagen='categorias_media/187.webp')
        cat2 = categorias.objects.create(nombre='Bebidas', imagen='categorias_media/7.webp')
        cat3 = categorias.objects.create(nombre='Postres', imagen='categorias_media/5.webp')

        self.stdout.write('Cargando Productos con sus categorías')
        prod1 = productos.objects.create(
            nombre= 'Enzalada de frutas', 
            descripcion=self.detalles, 
            precio=17.99, 
            categoria_fk=cat1,
            imagen='productos/175.webp'
        )
        prod2 = productos.objects.create(
            nombre= 'Pasta con champiñones', 
            descripcion=self.detalles, 
            precio=22.1, 
            categoria_fk=cat1,
            imagen='productos/178.webp'
        )
        prod3 = productos.objects.create(
            nombre= 'Champiñones rebosados', 
            descripcion=self.detalles, 
            precio=9.1, 
            categoria_fk=cat1,
            imagen='productos/178.webp'
        )
        prod4 = productos.objects.create(
            nombre= 'Pizza Italiana', 
            descripcion=self.detalles, 
            precio=10.1, 
            categoria_fk=cat1,
            imagen='productos/180.webp'
        )
        prod5 = productos.objects.create(
            nombre= 'Pizza Napolitana', 
            descripcion=self.detalles, 
            precio=15.1, 
            categoria_fk=cat1,
            imagen='productos/180.webp'
        )
        prod6 = productos.objects.create(
            nombre= 'Costilla', 
            descripcion=self.detalles, 
            precio=10.1, 
            categoria_fk=cat1,
            imagen='productos/189.webp'
        )
        prod7 = productos.objects.create(
            nombre= 'Hamburguesa', 
            descripcion=self.detalles, 
            precio=8, 
            categoria_fk=cat1,
            imagen='productos/186.webp'
        )
        # Bebidas
        prod8 = productos.objects.create(
            nombre= 'Café con leche', 
            descripcion=self.detalles, 
            precio=5.5, 
            categoria_fk=cat2,
            imagen='productos/1.webp'
        )
        prod9 = productos.objects.create(
            nombre= 'Café Negro', 
            descripcion=self.detalles, 
            precio=5.5, 
            categoria_fk=cat2,
            imagen='productos/1.webp'
        )
        prod10 = productos.objects.create(
            nombre= 'Campagne', 
            descripcion=self.detalles, 
            precio=20.8, 
            categoria_fk=cat2,
            imagen='productos/2.webp'
        )
        prod11 = productos.objects.create(
            nombre= 'Bebidas mixtas', 
            descripcion=self.detalles, 
            precio=10, 
            categoria_fk=cat2,
            imagen='productos/3.webp'
        )
        prod12 = productos.objects.create(
            nombre= 'Bebidas calientes mixtas', 
            descripcion=self.detalles, 
            precio=15.1, 
            categoria_fk=cat2,
            imagen='productos/4.webp'
        )
        prod13 = productos.objects.create(
            nombre= 'Vino', 
            descripcion=self.detalles, 
            precio=6, 
            categoria_fk=cat2,
            imagen='productos/6.webp'
        )
        prod14 = productos.objects.create(
            nombre= 'Frappe', 
            descripcion=self.detalles, 
            precio=7, 
            categoria_fk=cat2,
            imagen='productos/7.webp'
        )
        # Postres
        prod15 = productos.objects.create(
            nombre= 'Postre', 
            descripcion=self.detalles, 
            precio=9, 
            categoria_fk=cat3,
            imagen='productos/5.webp'
        )

        self.stdout.write('Creando mesas...')
        mes1 = mesas.objects.create(numero_mesa=1, estatus = 'ocupado')
        mes2 = mesas.objects.create(numero_mesa=2, estatus = 'disponible')
        mes3 = mesas.objects.create(numero_mesa=3, estatus = 'ocupado')
        mes4 = mesas.objects.create(numero_mesa=4, estatus = 'disponible')
        mes5 = mesas.objects.create(numero_mesa=5, estatus = 'ocupado')
        mes6 = mesas.objects.create(numero_mesa=6, estatus = 'disponible')

        self.stdout.write('Creando usuarios...')
        us1 = usuarios.objects.create(
            is_superuser = False,
            username = 'HolasoyMundo',
            first_name = 'Hola',
            last_name = 'Mundo',
            email = 'holamundo@hotmail.com',
            is_staff = False,
            is_active = True,
            role = 'cliente',
            imagen = 'usuarios_media/usuario1.webp'
        )
        us1.set_password('HolaMundo18')
        us1.save()
        us2 = usuarios.objects.create(
            is_superuser = False,
            username = 'CooperA',
            first_name = 'Cooper',
            last_name = 'Alexander',
            email = 'cooper24@gmail.com',
            is_staff = False,
            is_active = True,
            role = 'mesero',
            imagen = 'usuarios_media/usuario2.webp'
        )
        us2.set_password('Cooper245678')
        us2.save()
        us3 = usuarios.objects.create(
            is_superuser = False,
            username = 'XavierL',
            first_name = 'Xavier',
            last_name = 'Lara',
            email = 'xavier@gmail.com',
            is_staff = False,
            is_active = True,
            role = 'cajero',
            imagen = 'usuarios_media/usuario3.webp'
        )
        us3.set_password('XavierL123456')
        us3.save()
        us4 = usuarios.objects.create(
            is_superuser = False,
            username = 'IsRam',
            first_name = 'Issac',
            last_name = 'Ramirez',
            email = 'issacram@gmail.com',
            is_staff = False,
            is_active = True,
            role = 'admin',
            imagen = 'usuarios_media/usuario4.webp'
        )
        us4.set_password('isRam200026')
        us4.save()
        us5 = usuarios.objects.create(
            is_superuser = False,
            username = 'Asvg18',
            first_name = 'Angel',
            last_name = 'Vera',
            email = 'angelvera@outlook.com',
            is_staff = False,
            is_active = True,
            role = 'cliente',
            imagen = 'usuarios_media/usuario5.webp'
        )
        us5.set_password('asvg200518')
        us5.save()


        # Categorias ya, productos ya mesas ya usuarios ya
        # Falta comentarios ordenes detallesOrdenes
        self.stdout.write('Creando las ordenes...')
        ordn1 = ordenes.objects.create(
            estatus='pidiendo', 
            mesa_fk=mes1,
            monto_total = Decimal('0.00'),
            mesero = us2,
            cliente = us1
        )
        ordn2 = ordenes.objects.create(
            estatus='cocinando', 
            mesa_fk=mes3,
            monto_total = Decimal('0.00'),
            mesero = us2,
            cliente = us5
        )
        ordn3 = ordenes.objects.create(
            estatus='finalizado', 
            mesa_fk=mes5,
            monto_total = Decimal('0.00'),
            mesero = us2,
            cliente = us4
        )

        self.stdout.write('Creando los detalles de las ordenes...')
        detallesOrdenes.objects.create(
            producto_fk = prod1,
            precio = Decimal(prod1.precio),
            cantidad = 3,
            orden_fk = ordn1
        )
        detallesOrdenes.objects.create(
            producto_fk = prod2,
            precio = Decimal(prod2.precio),
            cantidad = 2,
            orden_fk = ordn1
        )
        detallesOrdenes.objects.create(
            producto_fk = prod15,
            precio = Decimal(prod15.precio),
            cantidad = 1,
            orden_fk = ordn1
        )

        detallesOrdenes.objects.create(
            producto_fk = prod4,
            precio = Decimal(prod4.precio),
            cantidad = 4,
            orden_fk = ordn2
        )
        detallesOrdenes.objects.create(
            producto_fk = prod7,
            precio = Decimal(prod7.precio),
            cantidad = 2,
            orden_fk = ordn2
        )
        detallesOrdenes.objects.create(
            producto_fk = prod14,
            precio = Decimal(prod14.precio),
            cantidad = 5,
            orden_fk = ordn2
        )
        detallesOrdenes.objects.create(
            producto_fk = prod15,
            precio = Decimal(prod15.precio),
            cantidad = 1,
            orden_fk = ordn2
        )

        detallesOrdenes.objects.create(
            producto_fk = prod6,
            precio = Decimal(prod6.precio),
            cantidad = 6,
            orden_fk = ordn3
        )
        detallesOrdenes.objects.create(
            producto_fk = prod8,
            precio = Decimal(prod8.precio),
            cantidad = 10,
            orden_fk = ordn3
        )

        self.stdout.write('Creando comentarios...')
        comentarios.objects.create(
            descripcion = 'Me encanta esta comida, excelente calidad',
            likes = int(25),
            estatus = True,
            usuario_fk = us2,
            producto_fk = prod1
        )
        comentarios.objects.create(
            descripcion = 'Sabroso el postre de fresas, nunca había probado algo igual',
            likes = int(40),
            estatus = True,
            usuario_fk = us3,
            producto_fk = prod15
        )
        comentarios.objects.create(
            descripcion = 'De lo mejor que probado en mucho tiempo',
            likes = int(10),
            estatus = True,
            usuario_fk = us3,
            producto_fk = prod5
        )
        comentarios.objects.create(
            descripcion = 'Buenisimo, recomendado',
            likes = int(5),
            estatus = True,
            usuario_fk = us3,
            producto_fk = prod6
        )
        comentarios.objects.create(
            descripcion = 'Espectacular',
            likes = int(7),
            estatus = True,
            usuario_fk = us4,
            producto_fk = prod8
        )
        comentarios.objects.create(
            descripcion = 'Totalmente recomendado',
            likes = int(11),
            estatus = True,
            usuario_fk = us5,
            producto_fk = prod12
        )

        favoritos.objects.create(
            usuario_fk = us1,
            producto_fk = prod15,
        )
        favoritos.objects.create(
            usuario_fk = us1,
            producto_fk = prod14,
        )
        favoritos.objects.create(
            usuario_fk = us1,
            producto_fk = prod13,
        )
        favoritos.objects.create(
            usuario_fk = us1,
            producto_fk = prod12,
        )

        favoritos.objects.create(
            usuario_fk = us2,
            producto_fk = prod1,
        )
        favoritos.objects.create(
            usuario_fk = us2,
            producto_fk = prod2,
        )

        favoritos.objects.create(
            usuario_fk = us3,
            producto_fk = prod3,
        )
        favoritos.objects.create(
            usuario_fk = us3,
            producto_fk = prod4,
        )
        favoritos.objects.create(
            usuario_fk = us3,
            producto_fk = prod15,
        )

        favoritos.objects.create(
            usuario_fk = us4,
            producto_fk = prod5,
        )
        favoritos.objects.create(
            usuario_fk = us4,
            producto_fk = prod4,
        )
        favoritos.objects.create(
            usuario_fk = us4,
            producto_fk = prod15,
        )
        favoritos.objects.create(
            usuario_fk = us4,
            producto_fk = prod3,
        )
        favoritos.objects.create(
            usuario_fk = us4,
            producto_fk = prod7,
        )
        favoritos.objects.create(
            usuario_fk = us4,
            producto_fk = prod12,
        )

        self.stdout.write(self.style.SUCCESS('Base de datos lista con informacion'))