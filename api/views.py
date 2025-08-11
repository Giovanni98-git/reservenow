from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import User, TableSalon, Reservation, Menu, Notification, Rapport, Horaire
from .serializers import (
    UserSerializer, TableSalonSerializer, ReservationSerializer,
    MenuSerializer, NotificationSerializer, RapportSerializer, HoraireSerializer
)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Lecture pour tous, édition pour auth

class TableSalonViewSet(viewsets.ModelViewSet):
    queryset = TableSalon.objects.all()
    serializer_class = TableSalonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [IsAdmin]

class HoraireViewSet(viewsets.ModelViewSet):
    queryset = Horaire.objects.all()
    serializer_class = HoraireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]