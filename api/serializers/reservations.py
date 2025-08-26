from rest_framework import serializers
from api.models import Reservation
from .tableSaloons import TableSaloonSerializer

class ReservationSerializer(serializers.ModelSerializer):
    table_saloons = TableSaloonSerializer(many=True, read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'