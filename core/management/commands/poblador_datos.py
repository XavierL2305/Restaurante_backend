from django.core.management.base import BaseCommand
from core.models import categorias, productos, mesas, usuarios, comentarios, ordenes, detallesOrdenes

class Command(BaseCommand):
    help = 'Poblando la base de datos con datos de prueba'
    detalles = "Aca es donde se detalla el producto (Comida, bebida...)"
    def handle(self, *args, **options):
        self.stdout.write('Borrando datos anteriores')
        # usuarios.objects.all().delete()
        categorias.objects.all().delete()
        productos.objects.all().delete()
        mesas.objects.all().delete()
        usuarios.objects.all().delete()
        ordenes.objects.all().delete()

        self.stdout.write('Creando categorías...')
        cat1 = categorias.objects.create(nombre='Platos Fuertes')
        cat2 = categorias.objects.create(nombre='Bebidas')
        cat3 = categorias.objects.create(nombre='Postres')

        self.stdout.write('Cargando Productos con sus categorías')
        productos.objects.create(
            nombre= 'Enzalada de frutas', 
            descripcion=self.detalles, 
            precio=17.99, 
            categoria_fk=cat1,
            imagen='productos/175.webp'
        )
        productos.objects.create(
            nombre= 'Pasta con champiñones', 
            descripcion=self.detalles, 
            precio=22.1, 
            categoria_fk=cat1,
            imagen='productos/178.webp'
        )
        productos.objects.create(
            nombre= 'Pasta con champiñones', 
            descripcion=self.detalles, 
            precio=9.1, 
            categoria_fk=cat1,
            imagen='productos/178.webp'
        )
        productos.objects.create(
            nombre= 'Pizza Italiana', 
            descripcion=self.detalles, 
            precio=10.1, 
            categoria_fk=cat1,
            imagen='productos/180.webp'
        )
        productos.objects.create(
            nombre= 'Pizza Napolitana', 
            descripcion=self.detalles, 
            precio=15.1, 
            categoria_fk=cat1,
            imagen='productos/180.webp'
        )
        productos.objects.create(
            nombre= 'Costilla', 
            descripcion=self.detalles, 
            precio=10.1, 
            categoria_fk=cat1,
            imagen='productos/189.webp'
        )
        productos.objects.create(
            nombre= 'Hamburguesa', 
            descripcion=self.detalles, 
            precio=8, 
            categoria_fk=cat1,
            imagen='productos/186.webp'
        )
        # Bebidas
        productos.objects.create(
            nombre= 'Café con leche', 
            descripcion=self.detalles, 
            precio=5.5, 
            categoria_fk=cat2,
            imagen='productos/1.webp'
        )
        productos.objects.create(
            nombre= 'Café con leche', 
            descripcion=self.detalles, 
            precio=5.5, 
            categoria_fk=cat2,
            imagen='productos/1.webp'
        )
        productos.objects.create(
            nombre= 'Campagne', 
            descripcion=self.detalles, 
            precio=20.8, 
            categoria_fk=cat2,
            imagen='productos/2.webp'
        )
        productos.objects.create(
            nombre= 'Bebidas mixtas', 
            descripcion=self.detalles, 
            precio=10, 
            categoria_fk=cat2,
            imagen='productos/3.webp'
        )
        productos.objects.create(
            nombre= 'Bebidas calientes mixtas', 
            descripcion=self.detalles, 
            precio=15.1, 
            categoria_fk=cat2,
            imagen='productos/4.webp'
        )
        productos.objects.create(
            nombre= 'Vino', 
            descripcion=self.detalles, 
            precio=6, 
            categoria_fk=cat2,
            imagen='productos/6.webp'
        )
        productos.objects.create(
            nombre= 'Frappe', 
            descripcion=self.detalles, 
            precio=7, 
            categoria_fk=cat2,
            imagen='productos/7.webp'
        )
        # Postres
        productos.objects.create(
            nombre= 'Postre', 
            descripcion=self.detalles, 
            precio=9, 
            categoria_fk=cat3,
            imagen='productos/5.webp'
        )

        self.stdout.write('Creando mesas...')
        cat1 = mesas.objects.create(numero_mesa=1, estatus = 'ocupado')
        cat2 = mesas.objects.create(numero_mesa=2, estatus = 'disponible')
        cat3 = mesas.objects.create(numero_mesa=3, estatus = 'ocupado')
        cat3 = mesas.objects.create(numero_mesa=4, estatus = 'disponible')
        cat3 = mesas.objects.create(numero_mesa=5, estatus = 'ocupado')
        cat3 = mesas.objects.create(numero_mesa=6, estatus = 'disponible')

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


        self.stdout.write(self.style.SUCCESS('Base de datos lista con informacion'))