from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.cart import CartViewSet

router = SimpleRouter()
router.register(
    'cart',
    CartViewSet,
    basename='cart'
)


urlpatterns = [
    path('', include(router.urls))
]
