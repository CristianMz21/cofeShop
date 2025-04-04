from django.test import TestCase, Client
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Product, Order

User = get_user_model()

class APITests(TestCase):
    """Pruebas para los endpoints del API"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            user_type='customer'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.category = Category.objects.create(
            name='Café',
            description='Diferentes tipos de café'
        )
        self.product = Product.objects.create(
            name='Café Colombiano',
            description='Café de origen colombiano',
            price=Decimal('12.99'),
            category=self.category,
            stock=50,
            available=True
        )

    def test_product_list(self):
        """Prueba el endpoint de lista de productos"""
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        """Prueba el endpoint de detalle de producto"""
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        """Prueba el endpoint para añadir producto al carrito"""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_checkout_authenticated(self):
        """Prueba el endpoint de checkout con usuario autenticado"""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('checkout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_order_management(self):
        """Prueba el endpoint de gestión de pedidos para administradores"""
        self.client.login(username='admin', password='adminpassword')
        url = reverse('order_management')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_inventory_management(self):
        """Prueba el endpoint de gestión de inventario para administradores"""
        self.client.login(username='admin', password='adminpassword')
        url = reverse('inventory_management')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_user_registration(self):
        """Prueba el endpoint de registro de usuarios"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'user_type': 'customer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
    def test_cart_operations(self):
        """Prueba operaciones básicas del carrito"""
        self.client.login(username='testuser', password='testpassword')
        # Añadir producto
        add_url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(add_url)
        self.assertEqual(response.status_code, 302)
        
        # Ver carrito
        cart_url = reverse('view_cart')
        response = self.client.get(cart_url)
        self.assertEqual(response.status_code, 200)
        
        # Eliminar producto
        remove_url = reverse('remove_from_cart', args=[self.product.id])
        response = self.client.post(remove_url)
        self.assertEqual(response.status_code, 302)