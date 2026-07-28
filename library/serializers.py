from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Author, Books, Borrow, BorrowItem, Category


class UserSerializers(serializers.ModelSerializer):
    role=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('id','username','password','email',"role")
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
            "username":self.user.username,
            "email":self.user.email,
            "role":self.user.groups.first().name if self.user.groups.exists() else None
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
            "user",
            "user_Display",
            "created_at",
            "due_date",
            "status",
            "items",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        borrow = Borrow.objects.create(**validated_data)

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
    Book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "Book_count",
        ]
