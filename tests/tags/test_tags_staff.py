from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models.user import User
from products.models.product import Product
from products.models.tag import Tag


class ProductsTestCase(APITestCase):
    fixtures = ['fixtures/products.json']

    def setUp(self):
        self.staff_user = User.objects.get(user_id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.staff_user)
        self.product = Product.objects.get(pk=1)
        self.tag = Tag.objects.get(pk=1)

    def test_tags_get(self):
        url = reverse('tags-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_id_get(self):
        url = reverse("tags-detail", args=[self.tag.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tag_products(self):
        url = reverse("get_tag_products-list", args=[self.tag.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_tags_post(self):
    #     url = reverse("products-detail", args=[self.product.pk])
    #     put_data = {
    #         "name": "test",
    #         "slug": "test_test"
    #     }
    #     response = self.client.post(url, put_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_products_put(self):
    #     url = reverse("products-detail", args=[self.product.pk])
    #
    #     put_data = {
    #         "name": "test_name",
    #         "description": "test_description",
    #         "last_modified_date": "2023-11-29T08:32:18.157Z",
    #         "price": 100010.0,
    #         "quantity": 101.0,
    #         "product_image": "",
    #         "tags": [
    #         ],
    #         "categories": [
    #         ]
    #     }
    #     response = self.client.put(url, put_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_products_patch(self):
    #     url = reverse("products-detail", args=[self.product.pk])
    #
    #     put_data = {
    #         'name': 'test_name',
    #         "description": "test_description",
    #         "price": 100010.0,
    #         "quantity": 101.0
    #     }
    #     response = self.client.patch(url, put_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_products_delete(self):
    #     url = reverse("products-detail", args=[self.product.pk])
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
