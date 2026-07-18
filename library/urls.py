from django.urls import path
from .views import BookList, BookDetails

urlpatterns = [
  # path('check/', views.Check_available , name='Check_available'),
  path("api/books/",BookList.as_view() ,name="all_books"),
  path("api/books/<int:pk>/",BookDetails.as_view() ,name="book_details"),
]