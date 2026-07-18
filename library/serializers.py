from rest_framework import serializers
from .models import Books, BorrowItem, Borrow


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
    class Meta:
        model = BorrowItem
        fields = [

            "book",
            "quantity",
        ]


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        items = BorrowItemSerializer(many=True)
        fields = [
            "user",
            "created_at",
            "due_date",
            "status",
            "items",
        ]
