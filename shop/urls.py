from django.urls import path
from . import views

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
]