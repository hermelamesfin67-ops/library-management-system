from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Author, Books, Borrow, BorrowItem, Category

from django.db import transaction
from datetime import timedelta
from django.utils import timezone
User=get_user_model()
class UserSerializers(serializers.ModelSerializer):
    role=serializers.CharField(write_only=True)
    account_type=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=('id','username','password','email',"role","account_type")
        extra_kwargs={"password":{"write_only":True}}
    
    
    def create(self, validated_data):
        role=validated_data.pop("role")
        user=User.objects.create_user(**validated_data)

        group=Group.objects.get(name=role) 
        user.groups.add(group)
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):   
    
    def validate(self,attrs):
        data=super().validate(attrs)
        data["user"]={
            "id":self.user.id,
            "username":self.user.username,
            "email":self.user.email,
            "role":self.user.groups.first().name if self.user.groups.exists() else None,
            "account_type":(
                "Superuser"
                if self.user.is_superuser
                else "Staff"
                if self.user.is_staff
                else self.user.role
                   ), 
            }
    
        return data
    
class BookSerializers(serializers.ModelSerializer):
    author_display = serializers.CharField(
        source='author_name.name', read_only=True)
    category_display = serializers.CharField(
        source='category_name.name', read_only=True)

    class Meta:
        model = Books
        fields = [
            "id",
            "title",
            "author_display",
            "category_display",
            "category_name",
            "author_name",
            "total_copies",
            "available_copies",
            "image",
        ]

    def validate(self, attrs):
        if self.instance:
            total = attrs.get("total_copies", self.instance.total_copies)
            available = attrs.get("available_copies",
                                  self.instance.available_copies)
        else:
            total = attrs.get("total_copies")
            available = attrs.get("available_copies", total)
        if available > total:
            raise serializers.ValidationError(
                "available copies cannot be greater than total copies")
        return attrs

    def create(self, validate_data):
        validate_data["available_copies"] = validate_data["total_copies"]

        return Books.objects.create(**validate_data)


class BorrowItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(
        source='book.title', read_only=True)

    class Meta:
        model = BorrowItem
        fields = [
            "book",
            "borrow",
            "quantity",
            "book_title",
        ]


class BorrowSerializer(serializers.ModelSerializer):
    items = BorrowItemSerializer(many=True)
    user_Display=serializers.CharField(source='user.username',read_only=True)
        
    
    class Meta:
        model = Borrow
        items = BorrowItemSerializer(many=True)
        fields = [
            
            "user_Display",
            "created_at",
            "due_date",
            "status",
            "items",
        ]
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        borrow = Borrow.objects.create(
            user=self.context["request"].user,
            due_date=timezone.now()+timedelta(days=7),
            status="borrowed",
            **validated_data)

        for item_data in items_data:
            BorrowItem.objects.create(borrow=borrow, **item_data)

        return borrow


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "biography",
            "book_count",
            'image',

        ]

    def delete(self):
            Author.delete()
            return Response({'message': 'Author deleted successfully'}, status=204)


class CategorySerializers(serializers.ModelSerializer):
    Book_count = serializers.IntegerField(source="books.count", read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "icon",
            "Book_count",
        ]
