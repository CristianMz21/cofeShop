from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import auth_views as shop_auth_views
from . import views_admin
from .auth_views import AdminLoginView, admin_login_redirect

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/complete/<int:order_id>/', views.order_complete, name='order_complete'),
    path('orders/', views.order_history, name='order_history'),
    
    # Rutas de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='shop/logout.html'), name='logout'),
    path('register/', shop_auth_views.register, name='register'),
    
    # Rutas de autenticación administrativa
    path('manage/login/', AdminLoginView.as_view(), name='admin_login'),
    path('manage/', admin_login_redirect, name='admin_redirect'),
    
    # Rutas para restablecer contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='shop/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='shop/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'), name='password_reset_complete'),
    
    # Rutas administrativas
    path('manage/orders/', views_admin.order_management, name='order_management'),
    path('manage/orders/<int:order_id>/', views_admin.order_detail_admin, name='order_detail_admin'),
    path('manage/orders/<int:order_id>/update/', views_admin.update_order_status, name='update_order_status'),
    path('manage/orders/<int:order_id>/inventory/', views_admin.update_inventory, name='update_inventory'),
    path('manage/inventory/', views_admin.inventory_management, name='inventory_management'),
    path('manage/inventory/add-stock/', views_admin.add_stock, name='add_stock'),
]