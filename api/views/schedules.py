from rest_framework import viewsets
from api.models import Schedule
from api.serializers import ScheduleSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]