from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsLibrarianOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return (
            request.user.groups.filter(name="Librarian").exists()
        )
class IsLibrarian(BasePermission):
    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Librarian").exists()
        )