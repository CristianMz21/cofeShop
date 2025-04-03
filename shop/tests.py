from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from decimal import Decimal

User = get_user_model()

class ModelTests(TestCase):
    """Pruebas para los modelos de la aplicación"""
    
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            user_type='customer'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            name='Café',
            description='Diferentes tipos de café'
        )
        
        # Crear producto de prueba
        self.product = Product.objects.create(
            name='Café Colombiano',
            description='Café de origen colombiano',
            price=Decimal('12.99'),
            category=self.category,
            stock=50,
            available=True
        )
    
    def test_user_creation(self):
        """Prueba la creación de un usuario y sus métodos"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.is_customer())
        self.assertFalse(self.user.is_admin())
        self.assertFalse(self.user.is_employee())
    
    def test_category_creation(self):
        """Prueba la creación de una categoría"""
        self.assertEqual(self.category.name, 'Café')
        self.assertEqual(str(self.category), 'Café')
    
    def test_product_creation(self):
        """Prueba la creación de un producto"""
        self.assertEqual(self.product.name, 'Café Colombiano')
        self.assertEqual(self.product.price, Decimal('12.99'))
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(str(self.product), 'Café Colombiano')
    
    def test_cart_creation(self):
        """Prueba la creación de un carrito y sus items"""
        # Crear carrito
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(str(cart), f'Carrito de {self.user.username}')
        
        # Añadir item al carrito
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.get_total_price(), Decimal('25.98'))
        self.assertEqual(cart.get_total_price(), Decimal('25.98'))
    
    def test_order_creation(self):
        """Prueba la creación de una orden y sus items"""
        # Crear orden
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            address='Test Address 123',
            phone='123456789',
            total_amount=Decimal('25.98'),
            status='pending'
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'pending')
        
        # Añadir item a la orden
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            price=self.product.price,
            quantity=2
        )
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.get_total_price(), Decimal('25.98'))

class ViewTests(TestCase):
    """Pruebas para las vistas de la aplicación"""
    
    def setUp(self):
        # Crear cliente de prueba
        self.client = Client()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            user_type='customer'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            name='Café',
            description='Diferentes tipos de café'
        )
        
        # Crear productos de prueba
        self.product1 = Product.objects.create(
            name='Café Colombiano',
            description='Café de origen colombiano',
            price=Decimal('12.99'),
            category=self.category,
            stock=50,
            available=True
        )
        
        self.product2 = Product.objects.create(
            name='Café Brasileño',
            description='Café de origen brasileño',
            price=Decimal('10.99'),
            category=self.category,
            stock=30,
            available=True
        )
    
    def test_home_view(self):
        """Prueba la vista de la página principal"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/home.html')
        self.assertContains(response, 'Café Colombiano')
    
    def test_product_list_view(self):
        """Prueba la vista de lista de productos"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list.html')
        self.assertContains(response, 'Café Colombiano')
        self.assertContains(response, 'Café Brasileño')
    
    def test_product_list_by_category(self):
        """Prueba la vista de lista de productos filtrada por categoría"""
        response = self.client.get(reverse('product_list_by_category', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list.html')
        self.assertContains(response, 'Café Colombiano')
    
    def test_product_search(self):
        """Prueba la búsqueda de productos"""
        response = self.client.get(f"{reverse('product_list')}?q=Colombiano")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Café Colombiano')
        self.assertNotContains(response, 'Café Brasileño')
    
    def test_product_detail_view(self):
        """Prueba la vista de detalle de producto"""
        response = self.client.get(reverse('product_detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertContains(response, 'Café Colombiano')
        self.assertContains(response, '12.99')

class CartTests(TestCase):
    """Pruebas para las funcionalidades del carrito"""
    
    def setUp(self):
        # Crear cliente de prueba
        self.client = Client()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            user_type='customer'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            name='Café',
            description='Diferentes tipos de café'
        )
        
        # Crear producto de prueba
        self.product = Product.objects.create(
            name='Café Colombiano',
            description='Café de origen colombiano',
            price=Decimal('12.99'),
            category=self.category,
            stock=50,
            available=True
        )
        
        # Iniciar sesión
        self.client.login(username='testuser', password='testpassword')
    
    def test_cart_detail_view(self):
        """Prueba la vista del carrito"""
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/cart_detail.html')
    
    def test_add_to_cart(self):
        """Prueba añadir un producto al carrito"""
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart_detail'))
        
        # Verificar que el producto se añadió al carrito
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product)
        self.assertEqual(cart.items.first().quantity, 1)
    
    def test_add_to_cart_multiple(self):
        """Prueba añadir el mismo producto varias veces al carrito"""
        # Añadir el producto dos veces
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        
        # Verificar que la cantidad se incrementó
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)
    
    def test_remove_from_cart(self):
        """Prueba eliminar un producto del carrito"""
        # Añadir el producto al carrito
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        cart = Cart.objects.get(user=self.user)
        cart_item = cart.items.first()
        
        # Eliminar el producto del carrito
        response = self.client.get(reverse('remove_from_cart', args=[cart_item.id]))
        self.assertRedirects(response, reverse('cart_detail'))
        
        # Verificar que el carrito está vacío
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

class OrderTests(TestCase):
    """Pruebas para las funcionalidades de órdenes"""
    
    def setUp(self):
        # Crear cliente de prueba
        self.client = Client()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            user_type='customer'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            name='Café',
            description='Diferentes tipos de café'
        )
        
        # Crear producto de prueba
        self.product = Product.objects.create(
            name='Café Colombiano',
            description='Café de origen colombiano',
            price=Decimal('12.99'),
            category=self.category,
            stock=50,
            available=True
        )
        
        # Iniciar sesión
        self.client.login(username='testuser', password='testpassword')
        
        # Crear carrito y añadir producto
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
    
    def test_checkout_view(self):
        """Prueba la vista de checkout"""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/checkout.html')
    
    def test_create_order(self):
        """Prueba la creación de una orden"""
        # Datos para el formulario de checkout
        checkout_data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'address': 'Test Address 123',
            'phone': '123456789'
        }
        
        # Enviar formulario de checkout
        response = self.client.post(reverse('checkout'), checkout_data)
        
        # Verificar que se creó la orden
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.full_name, 'Test User')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
        self.assertEqual(order.items.first().quantity, 2)
        
        # Verificar que el carrito se vació
        self.assertEqual(self.cart.items.count(), 0)
        
        # Verificar redirección a la página de orden completada
        self.assertRedirects(response, reverse('order_complete', args=[order.id]))
    
    def test_order_history_view(self):
        """Prueba la vista de historial de órdenes"""
        # Crear una orden
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            address='Test Address 123',
            phone='123456789',
            total_amount=Decimal('25.98'),
            status='pending'
        )
        
        # Verificar la vista de historial de órdenes
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/order_history.html')
        # Verificamos solo que aparezca el ID de la orden en lugar del nombre del usuario
        self.assertContains(response, str(order.id))
