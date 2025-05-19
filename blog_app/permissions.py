from rest_framework.permissions import BasePermission

class IsAdminCanEdit(BasePermission):
    def has_permission(self, request, view):
        print("Authenticated:", request.user.is_authenticated)
        print("User Type:", request.user.user_type)
        print("Has blog.can_edit_blog:", request.user.has_perm('blog_app.can_edit_blog'))
        return (
            request.user.is_authenticated and
            request.user.user_type == 'admin' and
            request.user.has_perm('blog_app.can_edit_blog')
        )

class CanViewBlog(BasePermission):
    def has_permission(self, request, view):
        print("Authenticated:", request.user.is_authenticated)
        print("User Type:", request.user.user_type)
        print("Has blog.can_view_blog:", request.user.has_perm('blog_app.can_view_blog'))

        return (
            request.user.is_authenticated and
            request.user.user_type == 'user' or
            request.user.user_type == 'admin' and
            request.user.has_perm('blog_app.can_view_blog')
        )