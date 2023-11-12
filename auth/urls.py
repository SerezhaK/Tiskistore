from django.urls import path

from .views.token_create import CustomTokenCreateView
from .views.token_destroy import CustomTokenDestroyView

urlpatterns = [
    path('login/', CustomTokenCreateView.as_view(), name='token_create'),
    path('logout/', CustomTokenDestroyView.as_view(), name='token_destroy')
]
