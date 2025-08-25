from rest_framework import viewsets
from api.models import Report
from api.serializers import ReportSerializer

# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'admin'

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    #permission_classes = [IsAdmin]