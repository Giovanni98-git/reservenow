from rest_framework import serializers
from api.models import Reservation, TableSaloon
from .tableSaloons import TableSaloonSerializer

class ReservationSerializer(serializers.ModelSerializer):
    table_saloon = TableSaloonSerializer(read_only=True)
    table_saloon_id = serializers.PrimaryKeyRelatedField(
        queryset=TableSaloon.objects.all(), source='table_saloon', write_only=True
    )
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'date', 'start', 'end', 'people_count', 'status',
            'user', 'table_saloon', 'table_saloon_id', 'user_email'
        ]
        read_only_fields = ['user', 'status', 'table_saloon', 'user_email']  # Ajouter user comme read_only

    def validate(self, data):
        start = data.get("start")
        end = data.get("end")
        date = data.get("date")
        table_saloon = data.get("table_saloon")
        people_count = data.get("people_count")

        if start and end and end <= start:
            raise serializers.ValidationError(
                {"end": "L'heure de fin doit être supérieure à l'heure de début."}
            )

        if table_saloon and people_count and people_count > table_saloon.capacity:
            raise serializers.ValidationError(
                {"people_count": f"Le nombre de personnes ({people_count}) dépasse la capacité "
                                f"de la table/salon ({table_saloon.capacity})."}
            )

        if table_saloon and date and start and end:
            overlapping = Reservation.objects.filter(
                table_saloon=table_saloon,
                date=date,
                status__in=["pending", "completed"],
                start__lt=end,
                end__gt=start
            ).exclude(pk=self.instance.pk if self.instance else None)
            if overlapping.exists():
                raise serializers.ValidationError(
                    {"table_saloon_id": "La table/salon est déjà réservée sur cet intervalle."}
                )

        return data