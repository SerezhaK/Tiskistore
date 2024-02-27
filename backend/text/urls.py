from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TextViewSet

router = SimpleRouter()
router.register(
    'text',
    TextViewSet,
    basename='text'
)


urlpatterns = [
    path('', include(router.urls))
]
