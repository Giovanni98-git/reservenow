from rest_framework import serializers
from api.models import Reservation
from .tableSalons import TableSalonSerializer

class ReservationSerializer(serializers.ModelSerializer):
    table_salons = TableSalonSerializer(many=True, read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'