from rest_framework import viewsets
from api.models import Menu
from api.serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]