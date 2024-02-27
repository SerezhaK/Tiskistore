from rest_framework.viewsets import ModelViewSet

from .models import Text
from .permissions import ReadOnly
from .serializer import TextSerializer


class TextViewSet(ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    permission_classes = [ReadOnly]
