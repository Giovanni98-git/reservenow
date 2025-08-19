from rest_framework import serializers
from api.models import TableSalon

class TableSalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableSalon
        fields = '__all__'