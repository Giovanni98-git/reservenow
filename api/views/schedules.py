from rest_framework import viewsets, permissions
from rest_framework.permissions import DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema
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

    # --- Swagger documentation ---
    @swagger_auto_schema(responses={200: ScheduleSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """
        List all schedules.
        Accessible to any authenticated user.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: ScheduleSerializer})
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific schedule.
        Accessible to any authenticated user.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=ScheduleSerializer, responses={200: ScheduleSerializer})
    def create(self, request, *args, **kwargs):
        """
        Create a new schedule.
        Requires DjangoModelPermissions: add_schedule
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=ScheduleSerializer, responses={200: ScheduleSerializer})
    def update(self, request, *args, **kwargs):
        """
        Update a schedule.
        Requires DjangoModelPermissions: change_schedule
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        """
        Delete a schedule.
        Requires DjangoModelPermissions: delete_schedule
        """
        return super().destroy(request, *args, **kwargs)
