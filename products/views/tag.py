from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from products.models.tag import Tag
from products.serializers.tag import TagSerializer


class TagViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Tag.objects.prefetch_related('products')
    serializer_class = TagSerializer
    # permission_classes = []
    # pagination_class = None
