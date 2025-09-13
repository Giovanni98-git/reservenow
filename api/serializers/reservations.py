from rest_framework import serializers
from api.models import Reservation
from .tableSaloons import TableSaloonSerializer

class ReservationSerializer(serializers.ModelSerializer):
    table_saloon = TableSaloonSerializer(read_only=True) 
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        """Validation personnalisée pour s'assurer que end > start"""
        start = data.get("start")
        end = data.get("end")

        if start and end and end <= start:
            raise serializers.ValidationError(
                {"end": "L'heure de fin doit être supérieure à l'heure de début."}
            )

        return data
