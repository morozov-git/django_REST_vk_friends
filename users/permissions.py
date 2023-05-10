from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj == request.user
