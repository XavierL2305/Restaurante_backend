from django.contrib import admin
from .models import (
    usuarios, mesas, categorias, productos,
    ordenes, detallesOrdenes, comentarios, favoritos
)


@admin.register(usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('-date_joined',)


@admin.register(mesas)
class MesasAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_mesa', 'estatus')
    list_filter = ('estatus',)
    search_fields = ('numero_mesa',)


@admin.register(categorias)
class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estatus')
    list_filter = ('estatus',)
    search_fields = ('nombre',)


@admin.register(productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria_fk', 'estatus')
    list_filter = ('estatus', 'categoria_fk')
    search_fields = ('nombre',)


@admin.register(ordenes)
class OrdenesAdmin(admin.ModelAdmin):
    list_display = ('id', 'estatus', 'mesa_fk', 'mesero', 'cliente', 'monto_total', 'fecha_creacion')
    list_filter = ('estatus', 'fecha_creacion')
    search_fields = ('cliente__email', 'cliente__first_name', 'mesa_fk__numero_mesa')
    ordering = ('-fecha_creacion',)


@admin.register(detallesOrdenes)
class DetallesOrdenesAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto_fk', 'orden_fk', 'cantidad', 'subtotal', 'estatus')
    list_filter = ('estatus',)
    raw_id_fields = ('orden_fk', 'producto_fk')


@admin.register(comentarios)
class ComentariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_fk', 'producto_fk', 'likes', 'estatus')
    list_filter = ('estatus',)
    search_fields = ('usuario_fk__email', 'descripcion')
    raw_id_fields = ('usuario_fk', 'producto_fk')


@admin.register(favoritos)
class FavoritosAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_fk', 'producto_fk')
    raw_id_fields = ('usuario_fk', 'producto_fk')