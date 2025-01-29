from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'type', 'sub_type',
                  'price', 'stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_types_subtypes(self, data):
        type_subtype_map = {
            'Pharma': ['dental', 'facial', 'corporal', 'hands_feet'],
            'Selective': ['make_up', 'fragance', 'various'],
            'Consumption': ['hygiene', 'drugstore', 'daily'],
        }

        type = data.get('type')
        subtype = data.get('subtype')

        # Validate that this subtype bellongs to the correct type
        valid_subcategories = type_subtype_map.get(type, [])
        if subtype not in valid_subcategories:
            raise serializers.ValidationError(
                f"The subtype '{
                    subtype}' is not allowed for the type: '{type}'."
            )
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = ('order_id', 'created_at', 'user',
                  'status', 'items', 'total_price')


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
