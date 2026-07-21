from django.urls import path
from .views import (BookListCreateView, BookDetailView, AuthorListCreateView,
                 AuthorDetailView,CategoryListCreateView, CategoryDetailView,
                   BorrowListCreateView, BorrowDetailView,BorrowItemListView,BorrowItemDetailView,
                 )

from django.http import JsonResponse
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
  # path('check/', views.Check_available , name='Check_available'),
  path("api/books/",BookListCreateView.as_view() ,name="all_books"),
  path("api/books/<int:pk>/",BookDetailView.as_view() ,name="book_details"),
  path("api/authors/",AuthorListCreateView.as_view(),name="all_authors"),
  path("api/authors/<int:pk>/",AuthorDetailView.as_view(),name="author_details"),
  path("api/categories/",CategoryListCreateView.as_view(),name="all_categories"),
  path("api/borrows/",BorrowListCreateView.as_view(),name="all_borrows"),
  path("api/borrows/<int:pk>/",BorrowDetailView.as_view(),name="borrow_details"),
  path("api/borrows/<int:pk>/items/",BorrowItemListView.as_view(),name="borrow_items"),
  path("api/borrows/<int:pk>/items/<int:item_pk>/",BorrowItemDetailView.as_view(),name="borrow_item_details"),
  path("api/categories/<int:pk>/",CategoryDetailView.as_view(),name="category_details"),

  path("health-check/", lambda request: JsonResponse({"status": "ok"}), name="health-check"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)