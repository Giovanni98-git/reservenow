from rest_framework import serializers
from api.models import TableSaloon

class TableSaloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableSaloon
        fields = '__all__'