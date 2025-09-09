from rest_framework import viewsets, permissions
from drf_yasg.utils import swagger_auto_schema
from api.models import Report
from api.serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reports.

    Permissions:
    - Manager: full access to reports.
    - Admin / superuser: full access.
    - Other users (e.g., Clients) cannot access reports.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restrict access to users in the 'Manager' or 'Admin' groups, or superusers.
        """
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=['Manager', 'Admin']).exists():
            return Report.objects.all()
        return Report.objects.none()  # no access for other users

    def perform_create(self, serializer):
        """
        Optionally associate the creator as the user for the report.
        """
        serializer.save(user=self.request.user)

    # --- Swagger documentation ---
    @swagger_auto_schema(responses={200: ReportSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """
        List all reports.
        Accessible only to Managers, Admins, or superusers.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: ReportSerializer})
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific report.
        Accessible only to Managers, Admins, or superusers.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=ReportSerializer, responses={201: ReportSerializer})
    def create(self, request, *args, **kwargs):
        """
        Create a new report.
        Accessible only to Managers, Admins, or superusers.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=ReportSerializer, responses={200: ReportSerializer})
    def update(self, request, *args, **kwargs):
        """
        Update a report.
        Accessible only to Managers, Admins, or superusers.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        """
        Delete a report.
        Accessible only to Managers, Admins, or superusers.
        """
        return super().destroy(request, *args, **kwargs)
