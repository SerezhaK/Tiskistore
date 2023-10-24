from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.categories import CategoriesViewSet
from .views.products import ProductsViewSet
from .views.tag import TagViewSet

router = SimpleRouter()
router.register(
    'products',
    ProductsViewSet,
    basename='products'
)
router.register(
    'tags',
    TagViewSet,
    basename='tags'
)
router.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)

urlpatterns = [
    path('', include(router.urls))
]
