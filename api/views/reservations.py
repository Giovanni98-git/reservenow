from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from api.models import Reservation
from api.serializers import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reservations.

    Permissions:
    - Authenticated users can create reservations.
    - Users need appropriate DjangoModelPermissions for update, delete, and list actions.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Allow create action with only IsAuthenticated, others require DjangoModelPermissions.
        """
        if self.action in ['list', 'retrieve', 'update', 'destroy']:
            return [IsAuthenticated(), DjangoModelPermissions()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Automatically assign the current authenticated user as the reservation owner.
        """
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError({"user": "Utilisateur non authentifié."})
        serializer.save(user=self.request.user)

    @swagger_auto_schema(responses={200: ReservationSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """
        List all reservations.
        Requires DjangoModelPermissions: view_reservation
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: ReservationSerializer})
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific reservation.
        Requires DjangoModelPermissions: view_reservation
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=ReservationSerializer, responses={201: ReservationSerializer})
    def create(self, request, *args, **kwargs):
        """
        Create a new reservation.
        The current user is automatically assigned as the owner.
        Requires DjangoModelPermissions: add_reservation
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=ReservationSerializer, responses={200: ReservationSerializer})
    def update(self, request, *args, **kwargs):
        """
        Update a reservation.
        Requires DjangoModelPermissions: change_reservation
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        """
        Delete a reservation.
        Requires DjangoModelPermissions: delete_reservation
        """
        return super().destroy(request, *args, **kwargs)