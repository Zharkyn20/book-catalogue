from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.models import Book, Rating, Favorite


class BookSerializer(serializers.ModelSerializer):
    is_favorite = serializers.BooleanField(read_only=True)
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="full_name", read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "genre", "author", "average_rating", "is_favorite")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context["request"].user

        representation["is_favorite"] = False
        if user.is_authenticated:
            representation["is_favorite"] = Favorite.objects.filter(
                user=user, book=instance
            ).exists()
        return representation


class InlineRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "user", "rating", "comment")


class BookRetrieveSerializer(serializers.ModelSerializer):
    ratings = InlineRatingSerializer(many=True, read_only=True)
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="full_name", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context["request"].user

        representation["is_favorite"] = False
        if user.is_authenticated:
            representation["is_favorite"] = Favorite.objects.filter(
                user=user, book=instance
            ).exists()
        return representation


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ("user",)

    def validate(self, attrs):
        user = self.context["request"].user
        book = attrs["book"]
        if Rating.objects.filter(user=user, book=book).exists():
            raise ValidationError(
                {"message": "Вы уже оставляли рейтинг для этой книги"}
            )
        return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        exclude = ("user",)

    def validate(self, attrs):
        user = self.context["request"].user
        book = attrs["book"]
        if Favorite.objects.filter(user=user, book=book).exists():
            raise ValidationError({"message": "Вы уже добавили эту книгу в избранное"})
        return attrs
