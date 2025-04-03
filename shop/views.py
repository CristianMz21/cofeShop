from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem

# Vista de la página principal
def home(request):
    products = Product.objects.filter(available=True)[:8]  # Mostrar los primeros 8 productos
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'title': 'Bienvenido a CoffeeShop'
    }
    return render(request, 'shop/home.html', context)

# Vista de todos los productos
def product_list(request, category_id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    
    # Búsqueda de productos
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'title': 'Nuestros Productos'
    }
    return render(request, 'shop/product_list.html', context)

# Vista de detalle de producto
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    context = {
        'product': product,
        'title': product.name
    }
    return render(request, 'shop/product_detail.html', context)

# Vista del carrito de compras
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'title': 'Tu Carrito'
    }
    return render(request, 'shop/cart_detail.html', context)

# Añadir producto al carrito
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} añadido a tu carrito')
    return redirect('cart_detail')

# Eliminar producto del carrito
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    messages.success(request, 'Carrito actualizado')
    return redirect('cart_detail')

# Proceso de checkout
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        # Crear una nueva orden
        order = Order(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_amount=cart.get_total_price()
        )
        order.save()
        
        # Crear items de la orden
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        
        # Limpiar el carrito
        cart.items.all().delete()
        
        messages.success(request, 'Tu orden ha sido procesada correctamente')
        return redirect('order_complete', order_id=order.id)
    
    context = {
        'cart': cart,
        'title': 'Finalizar Compra'
    }
    return render(request, 'shop/checkout.html', context)

# Vista de orden completada
@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'title': 'Orden Completada'
    }
    return render(request, 'shop/order_complete.html', context)

# Vista de historial de órdenes
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
        'title': 'Mis Órdenes'
    }
    return render(request, 'shop/order_history.html', context)
