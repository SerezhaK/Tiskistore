from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models.product import Product
from products.models.tag import Tag


class TagsTestCase(APITestCase):
    fixtures = ['fixtures/tags.json']

    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.get(pk=1)
        self.tag = get_object_or_404(Tag, id=1)

    def test_tags_get(self):
        url = reverse('tags-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_id_get(self):
        url = reverse("tags-detail", args=[self.tag.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tag_products(self):
        url = reverse("tags-detail", args=[self.product.pk]) + "products/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tags_post(self):
        url = reverse("tags-list")
        post_data = {
            "name": "test",
            "slug": "test_test"
        }
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tags_put(self):
        url = reverse("tags-detail", args=[self.tag.pk])
        put_data = {
            "name": "test",
            "slug": "test_test"
        }
        response = self.client.put(url, put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tags_patch(self):
        url = reverse("tags-detail", args=[self.tag.pk])
        patch_data = {
            "name": "test",
            "slug": "test_test"
        }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tags_delete(self):
        url = reverse("tags-detail", args=[self.tag.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
