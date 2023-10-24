from djoser.views import TokenDestroyView


class CustomTokenDestroyView(TokenDestroyView):
    serializer_class = None
