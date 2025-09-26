from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    """
    Autorise uniquement les Managers, Admins ou superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.groups.filter(name__in=['Manager']).exists()
            )
        )

# --- Permissions personnalisées pour les managers ---
class IsManagerOrSuperUser(BasePermission):
    """
    Permission personnalisée pour autoriser les managers et superusers.
    """
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_superuser or 
            request.user.groups.filter(name='Manager').exists()
        )


class IsSuperUser(BasePermission):
    """
    Permission réservée uniquement aux superusers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsManager(BasePermission):
    """
    Permission réservée uniquement aux managers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Manager').exists()

