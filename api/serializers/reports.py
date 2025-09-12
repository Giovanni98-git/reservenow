from rest_framework import serializers
from api.models import Report

class ReportSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['user_email']
