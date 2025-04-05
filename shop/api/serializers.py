from rest_framework import serializers
from shop.models import Category, Product, Order, OrderItem, Cart, CartItem, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone', 'address', 'city']
        read_only_fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id', 
                 'image', 'image_url', 'stock', 'available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True}
        }
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
        
    def to_internal_value(self, data):
        """
        Handle image as URL string in incoming data.
        """
        # Check if we have an image as URL string
        image_url = data.get('image')
        is_url = isinstance(image_url, str) and (image_url.startswith('http') or image_url.startswith('/media/'))
        
        # If it's a URL, remove it from data to avoid validation errors
        if is_url:
            image_copy = data.copy() if isinstance(data, dict) else data
            if isinstance(image_copy, dict):
                image_copy.pop('image', None)
            return super().to_internal_value(image_copy)
        
        return super().to_internal_value(data)
        
    def create(self, validated_data):
        """Handle creating product with image from URL."""
        # Get original request data
        request_data = self.context.get('request').data
        image_url = request_data.get('image')
        
        # Create product without image first
        product = Product.objects.create(**validated_data)
        
        # Process image URL if provided
        if image_url and isinstance(image_url, str):
            try:
                if '/media/products/' in image_url:
                    # Format: /media/products/filename.jpg - extract filename
                    filename = image_url.split('/media/products/')[-1]
                    product.image = f'products/{filename}'
                elif 'products/' in image_url:
                    # Already in correct format
                    product.image = image_url
                else:
                    # Use the last part of the URL as filename
                    import os
                    filename = os.path.basename(image_url)
                    product.image = f'products/{filename}'
            except Exception as e:
                print(f"Error processing image URL: {e}")
                pass  # Silently continue if there's an error with the image
        
        product.save()
        return product
        
    def update(self, instance, validated_data):
        """Handle updating product with image from URL."""
        # Get original request data
        request_data = self.context.get('request').data
        image_url = request_data.get('image')
        
        # Update all fields from validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # Process image URL if provided
        if image_url and isinstance(image_url, str):
            try:
                if '/media/products/' in image_url:
                    # Format: /media/products/filename.jpg - extract filename
                    filename = image_url.split('/media/products/')[-1]
                    instance.image = f'products/{filename}'
                elif 'products/' in image_url:
                    # Already in correct format
                    instance.image = image_url
                else:
                    # Use the last part of the URL as filename
                    import os
                    filename = os.path.basename(image_url)
                    instance.image = f'products/{filename}'
            except Exception as e:
                print(f"Error processing image URL: {e}")
                pass  # Silently continue if there's an error with the image
                
        instance.save()
        return instance

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']
        read_only_fields = ['id']
    
    def get_total_price(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        return obj.get_total_price()

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']
        read_only_fields = ['id']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'email', 'address', 'phone', 
                 'total_amount', 'status', 'status_display', 'notes', 
                 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']