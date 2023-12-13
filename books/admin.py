from django.contrib import admin

from .models import Book, Genre, Rating, Favorite


class InlineRating(admin.TabularInline):
    model = Rating
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [InlineRating]

    list_display = ["id", "title", "author"]
    list_display_links = ["id", "title", "author"]
    readonly_fields = ["slug", "average_rating"]

    class Meta:
        model = Book
        fields = "__all__"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]

    class Meta:
        model = Genre
        fields = "__all__"
