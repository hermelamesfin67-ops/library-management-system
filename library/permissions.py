from rest_framework.permissions import BasePermission


class IsLibrarianOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return (
            request.user.groups.filter(name="Librarian").exists()
            or request.user.is_superuser
        )
