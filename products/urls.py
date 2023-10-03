from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.products import ProductsViewSet
from .views.tag import TagViewSet
from .views.categories import CategoriesViewSet

router = SimpleRouter()
router.register(
    'products',
    ProductsViewSet,
    basename='products'
)
router.register(
    'tag',
    TagViewSet,
    basename='tag'
)
router.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)

urlpatterns = [
    path('', include(router.urls))
]
