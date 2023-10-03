from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.products import ProductsViewSet

router = SimpleRouter()
router.register(
    'products',
    ProductsViewSet,
    basename='products'
)

urlpatterns = [
    path('', include(router.urls))
]
