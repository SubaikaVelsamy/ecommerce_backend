from rest_framework.permissions import BasePermission

class IsAdminOrSuperAdmin(BasePermission):
    message = "Only super admin can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['admin', 'super_admin']
        )
