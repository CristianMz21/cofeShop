from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from shop.models import Category, Product, Order, OrderItem, Cart, CartItem, User
from .serializers import (
    CategorySerializer, ProductSerializer, OrderSerializer, 
    OrderItemSerializer, CartSerializer, CartItemSerializer, UserSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    """Permiso personalizado que permite acceso de lectura a todos,
    pero solo permite escritura a administradores."""
    
    def has_permission(self, request, view):
        # Permitir GET, HEAD, OPTIONS a cualquier usuario
        if request.method in permissions.SAFE_METHODS:
            return True
        # Verificar si el usuario es administrador para métodos de escritura
        return request.user.is_authenticated and request.user.user_type == 'admin'

class IsOwnerOrAdmin(permissions.BasePermission):
    """Permiso que permite a los usuarios ver y modificar solo sus propios recursos,
    mientras que los administradores pueden acceder a todos."""
    
    def has_object_permission(self, request, view, obj):
        # Permitir acceso a administradores
        if request.user.is_authenticated and request.user.user_type == 'admin':
            return True
        
        # Verificar si el objeto pertenece al usuario
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filtrar por categoría
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        # Búsqueda por nombre o descripción
        query = self.request.query_params.get('q', None)
        if query is not None:
            queryset = queryset.filter(name__icontains=query) | queryset.filter(description__icontains=query)
        
        # Filtrar por disponibilidad
        available = self.request.query_params.get('available', None)
        if available is not None:
            queryset = queryset.filter(available=(available.lower() == 'true'))
        
        return queryset

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        # Solo mostrar el carrito del usuario autenticado
        return Cart.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Endpoint para obtener el carrito del usuario actual"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Añadir un producto al carrito"""
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response({'error': 'Se requiere product_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id, available=True)
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado o no disponible'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Eliminar un producto del carrito"""
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response({'error': 'Se requiere item_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item no encontrado en el carrito'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        # Administradores pueden ver todas las órdenes
        if user.user_type == 'admin' or user.user_type == 'employee':
            return Order.objects.all().order_by('-created_at')
        # Clientes solo ven sus propias órdenes
        return Order.objects.filter(user=user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Crear una nueva orden a partir del carrito actual"""
        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                return Response({'error': 'El carrito está vacío'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Crear la orden
            order_data = {
                'user': request.user,
                'full_name': request.data.get('full_name'),
                'email': request.data.get('email'),
                'address': request.data.get('address'),
                'phone': request.data.get('phone'),
                'total_amount': cart.get_total_price(),
                'status': 'pending'
            }
            
            # Validar datos requeridos
            required_fields = ['full_name', 'email', 'address', 'phone']
            missing_fields = [field for field in required_fields if not order_data.get(field)]
            
            if missing_fields:
                return Response(
                    {'error': f'Faltan campos requeridos: {", ".join(missing_fields)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order = Order.objects.create(**order_data)
            
            # Crear items de la orden
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
            
            # Limpiar el carrito
            cart.items.all().delete()
            
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Cart.DoesNotExist:
            return Response({'error': 'No se encontró el carrito'}, 
                            status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Actualizar el estado de una orden (solo para administradores)"""
        if not request.user.user_type in ['admin', 'employee']:
            return Response({'error': 'No tiene permisos para realizar esta acción'},
                            status=status.HTTP_403_FORBIDDEN)
        
        order = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({'error': f'Estado inválido. Opciones válidas: {valid_statuses}'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)