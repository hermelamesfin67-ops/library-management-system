import os
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(null=True, blank=True)
    book_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to='authors/', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Books(models.Model):

    title = models.CharField(max_length=100)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="books/", null=True, blank=True)

    def save(self, *args, **kwargs):
        # Delete old image when updating
        try:
            old = Books.objects.get(pk=self.pk)
            if old.image and old.image != self.image:
                if os.path.isfile(old.image.path):
                    os.remove(old.image.path)
        except Books.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete image file when model is deleted
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    STATUS_CHOICES = [
        ('returned', 'Returned'),
        ('borrowed', 'Borrowed'),
        ('overdue', 'Overdue'),

    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Returned")

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"


class BorrowItem(models.Model):
    borrow = models.ForeignKey(
        Borrow, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.book.available_copies >= self.quantity:
                self.book.available_copies -= self.quantity
                self.book.save()

            else:
                raise ValueError("Not enough available copies")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.book.title
