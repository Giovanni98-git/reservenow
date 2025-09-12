from rest_framework import serializers
from api.models import Notification
from .reservations import ReservationSerializer

class NotificationSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    reservation_details = ReservationSerializer(source='reservation', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user_email', 'reservation_details']
