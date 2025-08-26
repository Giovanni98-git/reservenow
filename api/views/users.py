from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from api.models import User
from api.serializers import RegisterSerializer, UserSerializer, AdminUpdateRoleSerializer
from api.permissions import IsAdmin, IsOwner

# --- Registration ---
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# --- manage user's profile ---
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

# --- user's list by admin ---
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# --- update user's role by admin ---
class AdminUpdateRoleView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUpdateRoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'pk'
