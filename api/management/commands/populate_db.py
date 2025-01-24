import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import User, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='test')

        # create products - name, desc, price, stock, image
        products = [
            Product(name="Shampoo", description=lorem_ipsum.paragraph(), type="Consumption", sub_type="hygiene", price=Decimal('12.99'), stock=4),
            Product(name="1 Million Per Homme", description=lorem_ipsum.paragraph(), type="Selective", sub_type="fragance", price=Decimal('70.99'), stock=6),
            Product(name="Skin Cream", description=lorem_ipsum.paragraph(), type="Pharma", sub_type="corporal", price=Decimal('15.99'), stock=11),
            Product(name="Toothpicks", description=lorem_ipsum.paragraph(), type="Consumption", sub_type="daily", price=Decimal('17.99'), stock=2),
            Product(name="Loreal powders 222", description=lorem_ipsum.paragraph(), type="Selective", sub_type="make_up", price=Decimal('350.99'), stock=4),
            Product(name="Dental floss 111", description=lorem_ipsum.paragraph(), type="Pharma", sub_type="dental", price=Decimal('500.05'), stock=0),
        ]

        # create products & re-fetch from DB
        Product.objects.bulk_create(products)
        products = Product.objects.all()


        # create some dummy orders tied to the superuser
        for _ in range(3):
            # create an Order with 2 order items
            order = Order.objects.create(user=user)
            for product in random.sample(list(products), 2):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1,3)
                )