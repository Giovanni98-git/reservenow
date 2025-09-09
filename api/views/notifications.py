from rest_framework import viewsets, permissions
from drf_yasg.utils import swagger_auto_schema
from api.models import Notification
from api.serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notifications.

    Permissions:
    - Manager/Admin: full access to all notifications.
    - Client: can only view their own notifications.
    - Superuser: full access.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset based on user's group.
        - Managers/Admins and superusers see all notifications.
        - Clients see only their own notifications.
        """
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=['Manager', 'Admin']).exists():
            return Notification.objects.all()
        # Clients can only see notifications linked to them
        return Notification.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Automatically assign the current authenticated user as the notification owner.
        """
        serializer.save(user=self.request.user)

    # --- Swagger documentation ---
    @swagger_auto_schema(responses={200: NotificationSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """
        List all notifications.
        Managers/Admins see all, Clients see only their own.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: NotificationSerializer})
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific notification.
        Permissions same as list.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=NotificationSerializer, responses={201: NotificationSerializer})
    def create(self, request, *args, **kwargs):
        """
        Create a new notification.
        The current user is automatically assigned.
        Accessible to Managers/Admins or superusers.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=NotificationSerializer, responses={200: NotificationSerializer})
    def update(self, request, *args, **kwargs):
        """
        Update a notification.
        Accessible to Managers/Admins or superusers.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        """
        Delete a notification.
        Accessible to Managers/Admins or superusers.
        """
        return super().destroy(request, *args, **kwargs)
