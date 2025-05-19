from rest_framework.permissions import BasePermission

class IsAdminCanEdit(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'admin' and
            request.user.has_perm('category.can_edit_category')
        )
    