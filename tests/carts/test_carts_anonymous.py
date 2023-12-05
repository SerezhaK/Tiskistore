from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models.product import Product


class CartTestCase(APITestCase):
    fixtures = ['fixtures/carts.json']

    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.get(pk=1)

    def test_cart_get(self):
        url = reverse('cart-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_to_cart(self):
        url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_product_id_get(self):
        post_url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        self.client.post(post_url, post_data)

        url = reverse("cart-detail", args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_put(self):
        post_url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        self.client.post(post_url, post_data)

        url = reverse("cart-detail", args=[self.product.pk])
        put_data = {
            "product": self.product,
            "amount": 111123456
        }
        response = self.client.put(url, put_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_patch(self):
        post_url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        self.client.post(post_url, post_data)

        url = reverse("cart-detail", args=[self.product.pk])
        patch_data = {
            "product": self.product,
            "amount": 111123456
        }
        response = self.client.put(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_delete(self):
        post_url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        self.client.post(post_url, post_data)

        url = reverse("cart-detail", args=[self.product])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
