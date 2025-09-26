from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from api.models import Reservation
from api.serializers import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reservations.
    
    Permissions basées sur DjangoModelPermissions:
    - add_reservation: créer une réservation
    - change_reservation: modifier/annuler une réservation  
    - delete_reservation: supprimer définitivement une réservation (staff/superuser seulement)
    - view_reservation: voir les réservations
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        """
        # Gestion spéciale pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Reservation.objects.none()
        
        queryset = super().get_queryset()
        
        # Les superusers, staff et managers voient toutes les réservations
        if (self.request.user.is_staff or 
            self.request.user.is_superuser or 
            self.request.user.groups.filter(name='Manager').exists()):
            return queryset
        
        # Les utilisateurs normaux ne voient que leurs réservations
        return queryset.filter(user__=self.request.user.id)

    def perform_create(self, serializer):
        """
        Automatically assign the current authenticated user as the reservation owner.
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a reservation - seulement pour staff/superuser.
        Les managers et utilisateurs normaux ne peuvent pas supprimer définitivement.
        """
        instance = self.get_object()
        
        # Seuls les staff et superusers peuvent supprimer définitivement
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {
                    "error": "Vous n'avez pas la permission de supprimer définitivement une réservation. Utilisez l'annulation à la place."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Actions personnalisées
    @swagger_auto_schema(method='post', responses={200: ReservationSerializer})
    @action(detail=True, methods=['post'], permission_classes=[DjangoModelPermissions])
    def cancel(self, request, pk=None):
        """
        Cancel a reservation (soft delete by changing status).
        Accessible à tous les utilisateurs avec la permission 'change_reservation'
        """
        reservation = self.get_object()
        
        # Vérifier les permissions spécifiques
        if not (request.user.is_staff or 
                request.user.is_superuser or 
                request.user.groups.filter(name='Manager').exists() or
                reservation.user == request.user):
            return Response(
                {"error": "Vous n'avez pas la permission d'annuler cette réservation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier si la réservation peut être annulée
        if reservation.status == Reservation.STATUS_CANCELED:
            return Response(
                {"error": "Cette réservation est déjà annulée."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Empêcher l'annulation d'une réservation terminée
        if reservation.status == Reservation.STATUS_COMPLETED:
            return Response(
                {"error": "Impossible d'annuler une réservation déjà terminée."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = Reservation.STATUS_CANCELED
        reservation.save()
        
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ReservationSerializer(many=True)})
    @action(detail=False, methods=['get'], permission_classes=[DjangoModelPermissions])
    def my_reservations(self, request):
        """
        Get current user's reservations.
        """
        # Gestion spéciale pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Response([])
            
        reservations = Reservation.objects.filter(user__id=request.user.id)
        page = self.paginate_queryset(reservations)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ReservationSerializer(many=True)})
    @action(detail=False, methods=['get'], permission_classes=[DjangoModelPermissions])
    def upcoming(self, request):
        """
        Get upcoming reservations (from today onward).
        """
        from django.utils import timezone
        
        # Gestion spéciale pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Response([])
            
        reservations = Reservation.objects.filter(
            date__gte=timezone.now().date(),
            status__in=[Reservation.STATUS_PENDING, Reservation.STATUS_COMPLETED]
        )
        
        # Filtrage supplémentaire pour les non-staff/non-managers
        if not (request.user.is_staff or 
                request.user.is_superuser or 
                request.user.groups.filter(name='Manager').exists()):
            reservations = reservations.filter(user__id=request.user.id)
        
        page = self.paginate_queryset(reservations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ReservationSerializer(many=True)})
    @action(detail=False, methods=['get'], permission_classes=[DjangoModelPermissions])
    def today(self, request):
        """
        Get today's reservations.
        """
        from django.utils import timezone
        
        # Gestion spéciale pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Response([])
            
        reservations = Reservation.objects.filter(
            date=timezone.now().date(),
            status__in=[Reservation.STATUS_PENDING, Reservation.STATUS_COMPLETED]
        )
        
        # Filtrage supplémentaire pour les non-staff/non-managers
        if not (request.user.is_staff or 
                request.user.is_superuser or 
                request.user.groups.filter(name='Manager').exists()):
            reservations = reservations.filter(user__id=request.user.id)
        
        page = self.paginate_queryset(reservations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ReservationSerializer(many=True)})
    @action(detail=False, methods=['get'], permission_classes=[DjangoModelPermissions])
    def active(self, request):
        """
        Get active reservations (pending and completed).
        """
        # Gestion spéciale pour la génération du schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Response([])
            
        reservations = Reservation.objects.filter(
            status__in=[Reservation.STATUS_PENDING, Reservation.STATUS_COMPLETED]
        )
        
        # Filtrage supplémentaire pour les non-staff/non-managers
        if not (request.user.is_staff or 
                request.user.is_superuser or 
                request.user.groups.filter(name='Manager').exists()):
            reservations = reservations.filter(user__id=request.user.id)
        
        page = self.paginate_queryset(reservations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)