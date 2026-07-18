from django.contrib import admin
from .models import Author, Books, Borrow, BorrowItem, Category

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'author_name',
                    'category_name',

                    'total_copies',
                    'available_copies',
                    )
    search_fields = ('title','author_name__name','category_name__name',)
    list_filter = (
        'author_name',
        'category_name',
        
        )

class BorrowItemInline(admin.TabularInline):
   model =BorrowItem
   extra= 1
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'created_at',
                    'due_date',
                    'status'
                    )
    list_filter = ('created_at', 'due_date')
    inlines=[BorrowItemInline]

