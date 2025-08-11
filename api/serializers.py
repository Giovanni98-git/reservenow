from rest_framework import serializers
from .models import User, TableSalon, Reservation, Menu, Notification, Rapport, Horaire

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TableSalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableSalon
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    table_salons = TableSalonSerializer(many=True, read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = '__all__'

class HoraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horaire
        fields = '__all__'