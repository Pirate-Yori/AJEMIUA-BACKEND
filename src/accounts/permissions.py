from rest_framework.permissions import BasePermission

class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Un admin est simplement un utilisateur ayant le rôle "admin"
        return request.user.roles.filter(type__iexact="admin").exists()
