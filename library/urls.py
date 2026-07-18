from django.urls import path
from .views import BookList, BookDetails
from django.http import JsonResponse

urlpatterns = [
  # path('check/', views.Check_available , name='Check_available'),
  path("api/books/",BookList.as_view() ,name="all_books"),
  path("api/books/<int:pk>/",BookDetails.as_view() ,name="book_details"),
  path("health-check/", lambda request: JsonResponse({"status": "ok"}), name="health-check"),
]