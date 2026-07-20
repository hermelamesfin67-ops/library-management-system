from django.urls import path
from .views import BookListCreateView, BookDetailView, AuthorListCreateView, AuthorDetailView
from django.http import JsonResponse
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
  # path('check/', views.Check_available , name='Check_available'),
  path("api/books/",BookListCreateView.as_view() ,name="all_books"),
  path("api/books/<int:pk>/",BookDetailView.as_view() ,name="book_details"),
  path("api/authors/",AuthorListCreateView.as_view(),name="all_authors"),
  path("api/authors/<int:pk>/",AuthorDetailView.as_view(),name="author_details"),
  path("health-check/", lambda request: JsonResponse({"status": "ok"}), name="health-check"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)