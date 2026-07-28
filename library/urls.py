from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AuthorDetailView,
    AuthorListCreateView,
    BookDetailView,
    BookListCreateView,
    BorrowDetailView,
    BorrowItemDetailView,
    BorrowItemListView,
    BorrowListCreateView,
    CategoryDetailView,
    CategoryListCreateView,
    UserProfileView,
    UserListView,
    UserCreateView,
    
    MyLogin,
)

urlpatterns = [
    # path('check/', views.Check_available , name='Check_available'),
    path("api/register/", UserCreateView.as_view(), name="register"),
    path("api/users/", UserListView.as_view(), name="all_users"),

    path("api/profile/", UserProfileView.as_view(), name="user_details"),
    path("api/books/", BookListCreateView.as_view(), name="all_books"),
    path("api/books/<int:pk>/", BookDetailView.as_view(), name="book_details"),
    path("api/authors/", AuthorListCreateView.as_view(), name="all_authors"),
    path("api/authors/<int:pk>/", AuthorDetailView.as_view(), name="author_details"),
    path("api/categories/", CategoryListCreateView.as_view(), name="all_categories"),
    path("api/borrows/", BorrowListCreateView.as_view(), name="all_borrows"),
    path("api/borrows/<int:pk>/", BorrowDetailView.as_view(), name="borrow_details"),
    path("api/borrows/<int:pk>/items/",
         BorrowItemListView.as_view(), name="borrow_items"),
    path("api/borrows/<int:pk>/items/<int:item_pk>/",
         BorrowItemDetailView.as_view(), name="borrow_item_details"),
    path("api/categories/<int:pk>/",
         CategoryDetailView.as_view(), name="category_details"),

    path("health-check/",
         lambda request: JsonResponse({"status": "ok"}), name="health-check"),
    path("api/login/", MyLogin.as_view(), name="login"),
    path("api/refresh/", TokenRefreshView.as_view(), name="refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
