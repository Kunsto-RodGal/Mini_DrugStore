from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Order, Product, User


# Create your tests here.
class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass',
        )
        self.normal_user = User.objects.create_user(
            username='user',
            password='userpass',
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.00,
            stock=10,
        )
        self.url = reverse('product-detail', kwargs={'product_id': self.product.pk})


    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_unauthorized_update_product(self):
        data = {"name": "Updated Product"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)