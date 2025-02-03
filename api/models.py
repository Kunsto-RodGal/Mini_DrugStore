import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Product(models.Model):

    class TypeChoices(models.TextChoices):
        PHARMA = 'Pharma'
        SELECTIVE = 'Selective'
        CONSUMPTION = 'Consumption'

    class SubTypeChoices(models.TextChoices):
        DENTAL = 'dental'
        FACIAL = 'facial'
        CORPORAL = 'corporal'
        HANDS_FEET = 'hands_feet'
        MAKE_UP = 'make_up'
        FRAGANCE = 'fragance'
        VARIOUS = 'various'
        HYGIENE = 'hygiene'
        DRUGSTORE = 'drugstore'
        DAILY = 'daily'

    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TypeChoices.choices)
    sub_type = models.CharField(max_length=20, choices=SubTypeChoices.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Order(models.Model):

    class StatusChoices(models.TextChoices):
        PEDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PEDING)
    products = models.ManyToManyField(
        Product, through='OrderItem', related_name='orders')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
