# from django.conf import settings

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# port = ":8000" if not settings.DOCKER else ""
# docs_url = f'http://127.0.0.1{port}/api/docs/'

urlpatterns = [
    # path('', RedirectView.as_view(url=docs_url)),
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('users.urls')),
    path('api/', include('order.urls')),
    path('api/', include('cart.urls')),
    path('api/auth/token/', include('auth.urls')),
    # path('api/phone_login/', include('phone_login.urls', namespace='phone_login'),),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
#
# urlpatterns += static(
#     settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
# )
