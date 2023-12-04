from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models.category import Category
from products.models.product import Product
from users.models.user import User


class OrdersTestCase(APITestCase):
    fixtures = ['fixtures/categories.json']

    def setUp(self):
        self.user = User.objects.get(user_id=2)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product1 = Product.objects.get(pk=1)
        self.product2 = Product.objects.get(pk=1)
        self.product3 = Product.objects.get(pk=1)
        self.category = get_object_or_404(Category, id=1)