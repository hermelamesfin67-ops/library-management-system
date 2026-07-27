# from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework. generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response

# from rest_framework.decorators import api_view
from .models import Author, Books, Borrow, BorrowItem, Category
from .permissions import IsLibrarianOrReadOnly
from .serializers import (
    AuthorSerializers,
    BookSerializers,
    BorrowItemSerializer,
    BorrowSerializer,
    CategorySerializers,
    UserSerializers,
)

# def Check_available(request):
#     books = Books.objects.all()
#     borrow = Borrow.objects.all()

#     if borrow is None:
#         return jsonResponse({"error": not borrow})
#     for b in books:
#         if b.quantity > b.available_copies:
#             return jsonResponse({"error", "not enough"})
#     return jsonResponse()


# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def Book_list(request,pk):
#     try:
#         book = Books.objects.get(id=pk)
#     except Books.DoesNotExist:
#         return Response({'error': 'Book not found'}, status=404)

#     if request.method == 'GET':
#         serializer = BookSerializers(book)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = BookSerializers(book,data=request.data)

#         if serializer.is_valid():
#             serializer.save()  # for post because created is in post
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#     elif request.method == 'PATCH':
#         serializer = BookSerializers(book, data=request.data ,partial=True)
#         if serializer.is_valid():
#             serializer.save()  # for post because created is in post
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         book.delete()
#         return Response({'message': 'Book deleted successfully'}, status=204)


# @api_view(['GET'])
# def Book_detail(request):
#     if request.method == 'GET':
#         books = Books.objects.all()
#         serializer = BookSerializers(5, many=True)

#         return Response(serializer.data)
class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class BookListCreateView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializers
    # permission_classes = [DjangoModelPermissions]
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializers
    permission_classes = [IsLibrarianOrReadOnly , IsAuthenticated]


class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class BorrowListCreateView(ListCreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class BorrowDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class BorrowItemListView(ListCreateAPIView):
    queryset = BorrowItem.objects.all()
    serializer_class = BorrowItemSerializer
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]


class BorrowItemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = BorrowItem.objects.all()
    serializer_class = BorrowItemSerializer
    permission_classes = [IsLibrarianOrReadOnly, IsAuthenticated]

#     def get(self, request):
#         books = Books.objects.all()
#         serializer = BookSerializers(books, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = BookSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class BookDetails(APIView):
#     def get(self, request, pk):
#         try:
#             books = Books.objects.get(pk=pk)
#         except Books.DoesNotExist:
#             return Response({"error": "Book not found"}, status=404)

#         serializer = BookSerializers(books)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         try:
#             books= Books.objects.get(pk=pk)
#         except Books.DoesNotExist:
#             return Response({"error": "Book not found"}, status=404)

#         serializer = BookSerializers(books, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)

#     def patch(self, request, pk):
#         try:
#             books= Books.objects.get(pk=pk)
#         except Books.DoesNotExist:
#             return Response({"error": "Book not found"}, status=404)

#         serializer = BookSerializers(books, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, pk):
#         try:
#             books = Books.objects.get(pk=pk)
#         except Books.DoesNotExist:
#             return Response({"errors": "Book not found"}, status=404)
#         books.delete()
#         return Response({'message': 'Book deleted successfully'})
