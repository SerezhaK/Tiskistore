from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from cart.models.cart import Cart
from products.models.product import Product
from users.models.user import User


class CartTestCase(APITestCase):
    fixtures = ['fixtures/carts.json']

    def setUp(self):
        self.user_owner = User.objects.get(user_id=1)
        self.client_owner = APIClient()
        self.client_owner.force_authenticate(user=self.user_owner)

        self.product = Product.objects.get(pk=1)
        self.cart = Cart.objects.get(pk=5)

    def test_cart_get(self):
        url = reverse('cart-list')
        response = self.client_owner.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        url = reverse('cart-list')
        post_data = {
            "product": self.product,
            "amount": 11
        }
        response = self.client_owner.post(url, post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cart_product_id_get(self):
        url = reverse("cart-detail", args=[self.product.pk])
        response = self.client_owner.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_cart_put(self):
    #     post_url = reverse('cart-list')
    #     post_data = {
    #         "product": self.product,
    #         "amount": 11
    #     }
    #     self.client_owner.post(post_url, post_data)
    #
    #     url = reverse("cart-detail", args=[self.product.pk])
    #     put_data = {
    #         "product": self.product,
    #         "amount": 111123456
    #     }
    #     response = self.client_owner.put(url, put_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_cart_patch(self):
    #     post_url = reverse('cart-list')
    #     post_data = {
    #         "product": self.product,
    #         "amount": 11
    #     }
    #     self.client_owner.post(post_url, post_data)
    #
    #     url = reverse("cart-detail", args=[self.product.pk])
    #     patch_data = {
    #         "product": self.product,
    #         "amount": 111123456
    #     }
    #     response = self.client_owner.put(url, patch_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_cart_delete(self):
    #     post_url = reverse('cart-list')
    #     post_data = {
    #         "product": self.product,
    #         "amount": 11
    #     }
    #     self.client_owner.post(post_url, post_data)
    #
    #     url = reverse("cart-detail", args=[self.product])
    #     response = self.client_owner.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #
