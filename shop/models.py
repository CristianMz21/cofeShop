from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Modelo de Usuario personalizado
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('employee', 'Empleado'),
        ('customer', 'Cliente'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='cofeshop_users'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='cofeshop_users'
    )
    
    def is_admin(self):
        return self.user_type == 'admin'
    
    def is_employee(self):
        return self.user_type == 'employee'
    
    def is_customer(self):
        return self.user_type == 'customer'

# Modelo de Categoría de Productos
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

# Modelo de Producto
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# Modelo de Orden/Pedido
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('processing', 'En Proceso'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Orden #{self.id} - {self.user.username}'

# Modelo de Detalle de Orden
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_total_price(self):
        return self.price * self.quantity

# Modelo de Carrito de Compras
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Carrito de {self.user.username}'
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

# Modelo de Item del Carrito
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_total_price(self):
        return self.product.price * self.quantity
