from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem, Product, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'is_staff',
            'is_superuser'
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'type',
            'sub_type',
            'price',
            'stock'
        )

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
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )


class OrderCreateSerializer(serializers.ModelSerializer):

    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def create(self, validated_data):
        order_items_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in order_items_data:
                OrderItem.objects.create(order=order, **item)

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('items')

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if order_items_data is not None:
                # Clear existing items
                instance.items.all().delete()
                # Recreate items with the updated data
                for item in order_items_data:
                    OrderItem.objects.create(order=instance, **item)

        return instance

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items'
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price'
        )


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
