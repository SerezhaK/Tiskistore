from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.user import UserViewSet

router = SimpleRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('', include(router.urls))
]
