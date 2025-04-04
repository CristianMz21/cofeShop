from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from .models import Order, Product, Category

# Función para verificar si el usuario es administrador o empleado
def is_admin_or_employee(user):
    return user.is_authenticated and (user.user_type == 'admin' or user.user_type == 'employee')

# Decorador personalizado para verificar si el usuario es admin o empleado
def admin_employee_required(view_func):
    # Usar la configuración de ADMIN_LOGIN_URL desde settings.py si está disponible
    from django.conf import settings
    login_url = getattr(settings, 'ADMIN_LOGIN_URL', 'admin_login')
    return user_passes_test(is_admin_or_employee, login_url=login_url)(view_func)

# Vista para la gestión de pedidos (solo para administradores y empleados)
@admin_employee_required
def order_management(request):
    # Obtener parámetros de filtrado
    status = request.GET.get('status', '')
    date_from_str = request.GET.get('date_from', '')
    date_to_str = request.GET.get('date_to', '')
    
    # Inicializar consulta
    orders = Order.objects.all().order_by('-created_at')
    
    # Aplicar filtros si se proporcionan
    if status:
        orders = orders.filter(status=status)
    
    # Filtrar por fecha
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date__gte=date_from)
        except ValueError:
            pass
    
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            # Añadir un día para incluir todo el día final
            date_to = date_to + timedelta(days=1)
            orders = orders.filter(created_at__date__lt=date_to)
        except ValueError:
            pass
    
    # Preparar contexto para la plantilla
    context = {
        'orders': orders,
        'status': status,
        'date_from': datetime.strptime(date_from_str, '%Y-%m-%d').date() if date_from_str else '',
        'date_to': datetime.strptime(date_to_str, '%Y-%m-%d').date() if date_to_str else '',
        'title': 'Gestión de Pedidos'
    }
    
    return render(request, 'shop/order_management.html', context)

# Vista para ver detalles de un pedido (solo para administradores y empleados)
@admin_employee_required
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order,
        'title': f'Detalle de Pedido #{order.id}'
    }
    
    return render(request, 'shop/order_detail_admin.html', context)

# Vista para actualizar el estado de un pedido
@admin_employee_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        
        # Obtener el nuevo estado y notas del formulario
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        # Validar que el estado sea válido
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status in valid_statuses:
            # Guardar el estado anterior para mensajes
            old_status = order.get_status_display()
            
            # Si el pedido pasa de pendiente a en proceso, actualizar el inventario
            if order.status == 'pending' and new_status == 'processing':
                # Actualizar el stock de cada producto en el pedido
                for item in order.items.all():
                    product = item.product
                    if product.stock >= item.quantity:
                        product.stock -= item.quantity
                        product.save()
                        messages.success(request, f'Stock de {product.name} actualizado. Nuevo stock: {product.stock}')
                    else:
                        messages.warning(request, f'No hay suficiente stock de {product.name}. Stock actual: {product.stock}')
                        return redirect('order_detail_admin', order_id=order_id)
            
            # Actualizar el pedido
            order.status = new_status
            order.notes = notes
            order.updated_at = timezone.now()
            order.save()
            
            messages.success(request, f'Estado del pedido actualizado de {old_status} a {order.get_status_display()}')
        else:
            messages.error(request, 'Estado de pedido no válido')
    
    return redirect('order_detail_admin', order_id=order_id)

# Vista para actualizar el inventario basado en un pedido
@admin_employee_required
def update_inventory(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        update_stock = request.POST.get('update_stock') == '1'
        
        if update_stock:
            # Actualizar el stock de cada producto en el pedido
            for item in order.items.all():
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()
                    messages.success(request, f'Stock de {product.name} actualizado. Nuevo stock: {product.stock}')
                else:
                    messages.warning(request, f'No hay suficiente stock de {product.name}. Stock actual: {product.stock}')
            
            # Si el pedido estaba pendiente, cambiarlo a en proceso
            if order.status == 'pending':
                order.status = 'processing'
                order.save()
                messages.info(request, 'El estado del pedido ha sido actualizado a En Proceso')
        
    return redirect('order_detail_admin', order_id=order_id)

# Vista para añadir stock a un producto
@admin_employee_required
def add_stock(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        
        try:
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            
            if quantity > 0:
                product.stock += quantity
                product.save()
                messages.success(request, f'Se han añadido {quantity} unidades al stock de {product.name}')
            else:
                messages.error(request, 'La cantidad debe ser mayor que cero')
                
        except ValueError:
            messages.error(request, 'Cantidad no válida')
        
    return redirect('inventory_management')

# Vista para la gestión de inventario
@admin_employee_required
def inventory_management(request):
    # Obtener parámetros de filtrado
    category_id = request.GET.get('category', '')
    query = request.GET.get('q', '')
    stock_filter = request.GET.get('stock', '')
    
    # Inicializar consulta
    products = Product.objects.all().order_by('name')
    
    # Aplicar filtros
    if category_id:
        products = products.filter(category_id=category_id)
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if stock_filter == 'low':
        products = products.filter(stock__lt=10)
    elif stock_filter == 'out':
        products = products.filter(stock=0)
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'category_id': int(category_id) if category_id else '',
        'query': query,
        'stock_filter': stock_filter,
        'title': 'Gestión de Inventario'
    }
    
    return render(request, 'shop/inventory_management.html', context)