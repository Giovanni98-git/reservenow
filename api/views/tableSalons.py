from rest_framework import viewsets, permissions
from api.models import TableSalon
from api.serializers import TableSalonSerializer

class TableSalonViewSet(viewsets.ModelViewSet):
    queryset = TableSalon.objects.all()
    serializer_class = TableSalonSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]