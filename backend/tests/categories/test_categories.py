from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models.category import Category
from products.models.product import Product
from users.models.user import User


class CategoriesTestCase(APITestCase):
    fixtures = ['fixtures/categories.json']

    def setUp(self):
        self.user = User.objects.get(user_id=2)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.get(pk=1)
        self.category = get_object_or_404(Category, id=1)

    def test_categories_get(self):
        url = reverse('categories-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_id_get(self):
        url = reverse("categories-detail", args=[self.category.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_products(self):
        url = reverse(
            "categories-detail",
            args=[self.product.pk]
        ) + "products/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_categories_post(self):
        url = reverse("categories-list")
        post_data = {
            "name": "test",
            "slug": "test_test"
        }
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_categories_put(self):
        url = reverse("categories-detail", args=[self.category.pk])
        put_data = {
            "name": "test",
            "slug": "test_test"
        }
        response = self.client.put(url, put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_categories_patch(self):
        url = reverse("categories-detail", args=[self.category.pk])
        patch_data = {
            "name": "test",
            "slug": "test_test"
        }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_categories_delete(self):
        url = reverse("categories-detail", args=[self.category.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
