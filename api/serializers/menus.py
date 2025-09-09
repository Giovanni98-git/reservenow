from rest_framework import serializers
from api.models import Menu

class MenuSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ['user_email']
