from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema

from api.models import User
from api.permissions import IsManagerOrSuperUser, IsSuperUser
from api.serializers import (
    RegisterSerializer, 
    UserSerializer, 
    UserUpdateSerializer,
    AdminAssignGroupSerializer, 
    AdminUserSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for a user to retrieve or update their own profile.
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={200: UserSerializer},
        operation_summary="Get current user profile"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer},
        operation_summary="Update current user profile"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer},
        operation_summary="Partial update current user profile"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


# --- Change password ---
class ChangePasswordView(generics.UpdateAPIView):
    """
    API endpoint for a user to change their password.
    Requires authentication.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={200: "Mot de passe mis à jour avec succès."},
        operation_summary="Change user password"
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={200: "Mot de passe mis à jour avec succès."},
        operation_summary="Change user password"
    )
    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)


# --- Deactivate own account ---
class DeactivateAccountView(generics.UpdateAPIView):
    """
    API endpoint for a user to deactivate their own account.
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={200: "Compte désactivé avec succès."},
        operation_summary="Deactivate own account"
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Désactiver le compte
        user.is_active = False
        user.save()
        
        return Response(
            {"detail": "Votre compte a été désactivé avec succès."}, 
            status=status.HTTP_200_OK
        )


# --- List all users (Managers et Superusers) ---
class UserListView(generics.ListAPIView):
    """
    API endpoint to list all users.
    Accessible to Managers and Superusers.
    """
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrSuperUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si c'est un manager (pas superuser), ne montrer que les non-superusers
        if self.request.user.groups.filter(name='Manager').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @swagger_auto_schema(
        responses={200: AdminUserSerializer(many=True)},
        operation_summary="List all users",
        operation_description="Requires Manager or Superuser privileges"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# --- Retrieve specific user (Managers et Superusers) ---
class UserRetrieveView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a specific user.
    Accessible to Managers and Superusers.
    """
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrSuperUser]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si c'est un manager (pas superuser), ne peut voir que les non-superusers
        if self.request.user.groups.filter(name='Manager').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @swagger_auto_schema(
        responses={200: AdminUserSerializer},
        operation_summary="Retrieve a specific user",
        operation_description="Requires Manager or Superuser privileges"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# --- Update specific user (Managers et Superusers avec restrictions) ---
class UserUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update a specific user.
    Accessible to Managers and Superusers with restrictions.
    """
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrSuperUser]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si c'est un manager (pas superuser), ne peut modifier que les non-superusers
        if self.request.user.groups.filter(name='Manager').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @swagger_auto_schema(
        request_body=AdminUserSerializer,
        responses={200: AdminUserSerializer},
        operation_summary="Update a specific user",
        operation_description="Requires Manager or Superuser privileges"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=AdminUserSerializer,
        responses={200: AdminUserSerializer},
        operation_summary="Partial update a specific user",
        operation_description="Requires Manager or Superuser privileges"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.get_object()
        current_user = self.request.user
        
        # Restrictions pour les managers
        if current_user.groups.filter(name='Manager').exists() and not current_user.is_superuser:
            # Un manager ne peut pas modifier le statut superuser
            if 'is_superuser' in serializer.validated_data:
                raise permissions.PermissionDenied(
                    "Les managers ne peuvent pas modifier le statut superuser."
                )
        
        serializer.save()


# --- Assign group to a user (Managers et Superusers avec restrictions) ---
class AdminAssignGroupView(generics.UpdateAPIView):
    """
    API endpoint to assign groups to a user.
    Accessible to Managers and Superusers with restrictions.
    """
    queryset = User.objects.all()
    serializer_class = AdminAssignGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrSuperUser]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si c'est un manager (pas superuser), ne peut modifier que les non-superusers
        if self.request.user.groups.filter(name='Manager').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @swagger_auto_schema(
        request_body=AdminAssignGroupSerializer,
        responses={200: AdminAssignGroupSerializer},
        operation_summary="Assign groups to user",
        operation_description="Requires Manager or Superuser privileges"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=AdminAssignGroupSerializer,
        responses={200: AdminAssignGroupSerializer},
        operation_summary="Partial update groups for user",
        operation_description="Requires Manager or Superuser privileges"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        groups = serializer.validated_data.get('groups', [])
        instance = self.get_object()
        current_user = self.request.user

        # Seuls les superusers peuvent modifier les groupes des superusers
        if instance.is_superuser and not current_user.is_superuser:
            raise permissions.PermissionDenied(
                "Seuls les superutilisateurs peuvent modifier les groupes d'un superutilisateur."
            )

        serializer.save()


# --- Activate/Deactivate user (Managers et Superusers avec restrictions) ---
class AdminUserActivationView(generics.UpdateAPIView):
    """
    API endpoint to activate or deactivate a user account.
    Accessible to Managers and Superusers with restrictions.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer  # AJOUTÉ
    permission_classes = [permissions.IsAuthenticated, IsManagerOrSuperUser]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si c'est un manager (pas superuser), ne peut modifier que les non-superusers
        if self.request.user.groups.filter(name='Manager').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @swagger_auto_schema(
        request_body=serializers.Serializer,
        responses={200: AdminUserSerializer},
        operation_summary="Activate or deactivate user account"
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        current_user = request.user
        
        # Empêcher la désactivation d'un superuser par un manager
        if user.is_superuser and current_user.groups.filter(name='Manager').exists() and not current_user.is_superuser:
            raise permissions.PermissionDenied(
                "Les managers ne peuvent pas désactiver un superutilisateur."
            )
        
        # Empêcher un utilisateur de se désactiver lui-même via cette endpoint
        if user == current_user:
            raise permissions.PermissionDenied(
                "Utilisez l'endpoint de désactivation de compte pour votre propre compte."
            )
        
        # Inverser le statut actif/inactif
        user.is_active = not user.is_active
        user.save()
        
        action = "activé" if user.is_active else "désactivé"
        serializer = AdminUserSerializer(user)
        
        return Response({
            "detail": f"Le compte de {user.email} a été {action} avec succès.",
            "user": serializer.data
        }, status=status.HTTP_200_OK)


# --- Delete user (Superusers seulement) ---
class UserDeleteView(generics.DestroyAPIView):
    """
    API endpoint to permanently delete a user (hard delete).
    Reserved for Superusers only.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    lookup_field = 'pk'

    @swagger_auto_schema(
        responses={204: 'No Content'},
        operation_summary="Permanently delete a user",
        operation_description="Requires Superuser privileges. Use with caution."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # Empêcher la suppression de son propre compte
        if instance == self.request.user:
            raise permissions.PermissionDenied(
                "Vous ne pouvez pas supprimer votre propre compte. Utilisez la désactivation."
            )
        
        instance.delete()


# --- Promote to superuser (Superusers seulement) ---
class PromoteToSuperuserView(generics.UpdateAPIView):
    """
    API endpoint to promote a user to superuser.
    Only accessible by superusers.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer  # AJOUTÉ
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    lookup_field = 'pk'

    @swagger_auto_schema(
        request_body=serializers.Serializer,
        responses={200: AdminUserSerializer},
        operation_summary="Promote user to superuser",
        operation_description="Requires Superuser privileges"
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        serializer = AdminUserSerializer(user)
        return Response(serializer.data)


# --- Promote to manager (Managers et Superusers) ---
class PromoteToManagerView(generics.UpdateAPIView):
    """
    API endpoint to promote a user to manager.
    Accessible to Managers and Superusers.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer  # AJOUTÉ
    permission_classes = [permissions.IsAuthenticated, IsManagerOrSuperUser]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si c'est un manager (pas superuser), ne peut promouvoir que les non-superusers
        if self.request.user.groups.filter(name='Manager').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @swagger_auto_schema(
        request_body=serializers.Serializer,
        responses={200: AdminUserSerializer},
        operation_summary="Promote user to manager",
        operation_description="Requires Manager or Superuser privileges"
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        current_user = self.request.user
        
        # Vérifier qu'un manager ne peut pas promouvoir un superuser
        if user.is_superuser and current_user.groups.filter(name='Manager').exists() and not current_user.is_superuser:
            raise permissions.PermissionDenied(
                "Les managers ne peuvent pas promouvoir un superutilisateur."
            )
        
        # Ajouter l'utilisateur au groupe Manager
        manager_group, created = Group.objects.get_or_create(name='Manager')
        user.groups.add(manager_group)
        user.is_staff = True  # Un manager est automatiquement staff
        user.save()
        
        serializer = AdminUserSerializer(user)
        return Response(serializer.data)


# --- Demote from manager (Managers et Superusers) ---
class DemoteFromManagerView(generics.UpdateAPIView):
    """
    API endpoint to demote a user from manager role.
    Accessible to Managers and Superusers.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer  # AJOUTÉ
    permission_classes = [permissions.IsAuthenticated, IsManagerOrSuperUser]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si c'est un manager (pas superuser), ne peut rétrograder que les non-superusers
        if self.request.user.groups.filter(name='Manager').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @swagger_auto_schema(
        request_body=serializers.Serializer,
        responses={200: AdminUserSerializer},
        operation_summary="Demote user from manager role",
        operation_description="Requires Manager or Superuser privileges"
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        current_user = self.request.user
        
        # Empêcher un manager de se rétrograder lui-même
        if user == current_user and current_user.groups.filter(name='Manager').exists() and not current_user.is_superuser:
            raise permissions.PermissionDenied(
                "Vous ne pouvez pas vous rétrograder vous-même."
            )
        
        # Vérifier qu'un manager ne peut pas rétrograder un superuser
        if user.is_superuser and current_user.groups.filter(name='Manager').exists() and not current_user.is_superuser:
            raise permissions.PermissionDenied(
                "Les managers ne peuvent pas rétrograder un superutilisateur."
            )
        
        # Retirer l'utilisateur du groupe Manager
        manager_group = Group.objects.filter(name='Manager').first()
        if manager_group and user.groups.filter(name='Manager').exists():
            user.groups.remove(manager_group)
            
            # Si l'utilisateur n'est pas superuser et n'a pas d'autres groupes staff, retirer is_staff
            if not user.is_superuser and not user.groups.filter(name__in=['Manager']).exists():
                user.is_staff = False
            
            user.save()
        
        serializer = AdminUserSerializer(user)
        return Response(serializer.data)


# --- View for current user ---
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    """
    API endpoint to get current user information.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)