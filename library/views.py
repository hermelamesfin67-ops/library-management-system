# from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework. generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import Author, Books, Borrow, Category
from .permissions import IsLibrarianOrReadOnly, IsLibrarian, IsSuperUser,  IsLibrarianOrStudent
from .serializers import (
    AuthorSerializers,
    BookSerializers,
    BorrowItemSerializer,
    BorrowSerializer,
    CategorySerializers,
    UserSerializers,
    MyTokenObtainPairSerializer,
)
from django.utils import timezone

User = get_user_model()


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_superuser or request.user.groups.filter(name="Librarian").exists()):
            my_borrows=Borrow.objects.filter(user=request.user)
            my_borrowed = my_borrows.filter(
                status="borrowed"
            ).count()
            my_returned = my_borrows.filter(
                status="returned"
            ).count()

            my_overdue = my_borrows.filter(
                status="borrowed",
                due_date__lt=timezone.now()
            ).count()

            return Response({
                "my_borrowed": my_borrowed,
                "my_returned": my_returned,
                "my_overdue": my_overdue,
            })
        
        total_users=User.objects.all().count()
        total_books=Books.objects.all().count()
        total_copies= sum(book.total_copies for book in Books.objects.all())
        available_copies= sum(book.available_copies for book in Books.objects.all())
        borrowed = total_copies - available_copies

        overdue = Borrow.objects.filter(
            status="borrowed",
            due_date__lt=timezone.now()
        ).count()

        return Response({
            "total_users": total_users,
            "total_books": total_books,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "borrowed": borrowed,
            "overdue": overdue,
            "chart": [
                {
                    "name": "Total Copies",
                    "value": total_copies
                },
                {
                    "name": "Available",
                    "value": available_copies
                },
                {
                    "name": "Borrowed",
                    "value": borrowed
                },
                {
                    "name": "Overdue",
                    "value": overdue
                }
            ]
        })
class MyLogin(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsSuperUser]


class UserCreateView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsSuperUser]


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsSuperUser]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=204
        )


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializers

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsSuperUser()]
        return [IsAuthenticated()]


class BookListCreateView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializers

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(),
                    IsLibrarian()]
        return [AllowAny()]


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializers

    def get_permissions(self):
        if self.request.method == "PUT":
            return [
                IsLibrarian()]
        elif self.request.method == "PATCH":
            return [
                IsLibrarian()]
        elif self.request.method == "DELETE":
            return [
                IsLibrarian()]
        return [
            AllowAny()
        ]


class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(),
                    IsLibrarian()]
        return [AllowAny()]


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
    permission_classes = [IsLibrarianOrReadOnly]


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(),
                    IsLibrarian()]
        return [AllowAny()]


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get_permissions(self):
        if self.request.method == "PUT":
            return [
                IsLibrarian()]
        elif self.request.method == "PATCH":
            return [
                IsLibrarian()]
        elif self.request.method == "DELETE":
            return [
                IsLibrarian()]

        return [
            AllowAny()
        ]


class BorrowListCreateView(ListCreateAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [IsLibrarianOrStudent]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Borrow.objects.all()

        if self.request.user.groups.filter(name="Librarian").exists():
            return Borrow.objects.all()

        return Borrow.objects.filter(user=self.request.user)


class BorrowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrReadOnly]

    @action(
        detail=True,
        methods=["patch"],
        url_path="return",
    )
    def return_book(self, request, pk=None):

        with transaction.atomic():

            borrow = Borrow.objects.select_for_update().get(pk=pk)

            # Prevent returning twice
            if borrow.status == "returned":
                return Response(
                    {"detail": "This borrow has already been returned."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Return each book's copies
            for item in borrow.items.select_related("book"):

                book = item.book

                book.available_copies += item.quantity

                # Don't exceed total copies
                if book.available_copies > book.total_copies:
                    book.available_copies = book.total_copies

                book.save(update_fields=["available_copies"])

            # Change borrow status
            borrow.status = "returned"
            borrow.save(update_fields=["status"])

            return Response(
                {
                    "detail": "Book returned successfully.",
                    "borrow_id": borrow.id,
                    "status": borrow.status
                },
                status=status.HTTP_200_OK
            )


class BorrowDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]
