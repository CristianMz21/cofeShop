from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Order, OrderItem, Cart, CartItem

# Personalización del admin para el modelo User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('user_type', 'phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('user_type', 'phone', 'address')}),
    )

# Registro de modelos en el admin
admin.site.register(User, CustomUserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información del Cliente', {'fields': ('user', 'full_name', 'email', 'phone', 'address')}),
        ('Información del Pedido', {'fields': ('total_amount', 'status', 'notes')}),
        ('Fechas', {'fields': ('created_at', 'updated_at')}),
    )
    inlines = [OrderItemInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
