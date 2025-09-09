from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    message = "You must be an administrator to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsOwner(BasePermission):
    message = "You can only edit your own data."

    def has_object_permission(self, request, view, obj):
        return obj == request.user