from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models.product import Product
from users.models.user import User


class OrdersTestCase(APITestCase):
    fixtures = ['fixtures/products.json']

    def setUp(self):
        self.user = User.objects.get(user_id=2)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.get(pk=1)
        self.product2 = Product.objects.get(pk=2)

    def test_cart_get(self):
        url = reverse('cart-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }

        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_product_id_get(self):
        post_url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        self.client.post(post_url, post_data, format='json')

        url = reverse("cart-detail", args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_put(self):
        post_url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        post_resp = self.client.post(post_url, post_data, format='json')

        url = reverse("cart-detail", args=[self.product.pk])
        put_data = {
            "amount": 111
        }
        response = self.client.put(url, put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_patch(self):
        post_url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        self.client.post(post_url, post_data, format='json')

        url = reverse("cart-detail", args=[self.product.pk])
        patch_data = {
            "amount": 111
        }
        response = self.client.put(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_delete(self):
        url = reverse("cart-detail", args=[self.product.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
