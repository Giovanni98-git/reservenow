from rest_framework import viewsets, permissions
from rest_framework.permissions import DjangoModelPermissions
from api.models import Schedule
from api.serializers import ScheduleSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing schedules.

    Permissions:
    - Client: can view schedules if assigned the view_schedule permission.
    - Manager: full access except for superuser-only operations.
    - Admin / superuser: full access.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_permissions(self):
        """
        Open list and retrieve endpoints to all authenticated users.
        Other actions require DjangoModelPermissions.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [DjangoModelPermissions()]