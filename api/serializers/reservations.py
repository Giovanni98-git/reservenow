from rest_framework import serializers
from api.models import Reservation
from .tableSaloons import TableSaloonSerializer

class ReservationSerializer(serializers.ModelSerializer):
    table_saloon = TableSaloonSerializer(read_only=True) 
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
