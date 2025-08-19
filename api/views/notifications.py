from rest_framework import viewsets
from api.models import Notification
from api.serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = [permissions.IsAuthenticated]