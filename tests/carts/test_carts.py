from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models.product import Product
from users.models.user import User


class CartsTestCase(APITestCase):
    fixturs = ['fixtures/products.json']

    def setUp(self):
        self.user = User.objects.get(user_id=2)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product1 = Product.objects.get(pk=1)
        self.product2 = Product.objects.get(pk=2)

    def test_products_get(self):
        url = reverse('products-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_id_get(self):
        url = reverse("products-detail", args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_post(self):
        url = reverse("products-detail", args=[self.product.pk])
        post_data = {
            "name": "test_post_name",
            "description": "test_post_description",
            "last_modified_date": "1000-10-10T00:00:00.157Z",
            "price": 111.0,
            "quantity": 111.0,
            "product_image": "",
            "tags": [
            ],
            "categories": [
            ]
        }
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_products_put(self):
        url = reverse("products-detail", args=[self.product.pk])

        put_data = {
            "name": "test_name",
            "description": "test_description",
            "last_modified_date": "2023-11-29T08:32:18.157Z",
            "price": 100010.0,
            "quantity": 101.0,
            "product_image": "",
            "tags": [
            ],
            "categories": [
            ]
        }
        response = self.client.put(url, put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_products_patch(self):
        url = reverse("products-detail", args=[self.product.pk])

        patch_data = {
            'name': 'test_name',
            "description": "test_description",
            "price": 100010.0,
            "quantity": 101.0
        }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_products_delete(self):
        url = reverse("products-detail", args=[self.product.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
