from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from api.models import User
from api.serializers import RegisterSerializer, UserSerializer, AdminAssignGroupSerializer

# --- User Registration ---
class RegisterView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    Open to anyone (AllowAny permission).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer},
        operation_summary="Register a new user",
        operation_description="Open to anyone"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# --- Manage own profile ---
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for a user to retrieve, update, or delete their own profile.
    Requires authentication.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={200: UserSerializer},
        operation_summary="Get current user profile"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer},
        operation_summary="Update current user profile"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


# --- List all users ---
class UserListView(generics.ListAPIView):
    """
    API endpoint to list all users.
    Requires Django model permissions (view_user).
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]

    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)},
        operation_summary="List all users",
        operation_description="Requires view_user permission"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# --- Assign group to a user (Admin or Manager) ---
class AdminAssignGroupView(generics.UpdateAPIView):
    """
    API endpoint to assign a group to a user.
    Only Managers or Admins can assign groups.
    Only superusers can assign the Admin group.
    """
    queryset = User.objects.all()
    serializer_class = AdminAssignGroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    @swagger_auto_schema(
        request_body=AdminAssignGroupSerializer,
        responses={200: AdminAssignGroupSerializer},
        operation_summary="Assign group to user",
        operation_description="Manager/Admin can assign groups. Only superuser can assign Admin group."
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        group = serializer.validated_data.get('group')

        # Only superusers can assign Admin group
        if group.name == 'Admin' and not self.request.user.is_superuser:
            raise PermissionError("Only superusers can assign the Admin group.")

        # Ensure the current user is Manager/Admin or superuser
        if not self.request.user.groups.filter(name__in=['Manager', 'Admin']).exists() and not self.request.user.is_superuser:
            raise PermissionError("Only Managers or Admins can assign groups.")

        serializer.save()
