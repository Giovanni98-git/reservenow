from rest_framework import viewsets
from api.models import Horaire
from api.serializers import HoraireSerializer

class HoraireViewSet(viewsets.ModelViewSet):
    queryset = Horaire.objects.all()
    serializer_class = HoraireSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]