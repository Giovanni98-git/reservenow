from rest_framework import viewsets
from api.models import Rapport
from api.serializers import RapportSerializer

# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'admin'

class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    #permission_classes = [IsAdmin]