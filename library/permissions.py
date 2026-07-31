from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLibrarianOrReadOnly(BasePermission):  # custom permission
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
            and (
                request.user.is_superuser
                or request.user.groups.filter(name="Librarian").exists()
            )
        )


class IsStudent(BasePermission):
    def has_permission(self, request, view):

        return (request.user.is_authenticated and request.user.is_superuser or request.user.role == "Member")


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):

        return (request.user.is_authenticated and request.user.is_superuser)
