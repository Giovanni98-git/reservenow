from rest_framework import serializers
from api.models import Rapport

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = '__all__'