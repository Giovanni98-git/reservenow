from rest_framework import viewsets, permissions
from api.models import TableSaloon
from api.serializers import TableSaloonSerializer

class TableSaloonViewSet(viewsets.ModelViewSet):
    queryset = TableSaloon.objects.all()
    serializer_class = TableSaloonSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]