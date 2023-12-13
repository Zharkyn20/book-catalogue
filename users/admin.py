from django.contrib import admin

from books.models import Favorite
from .models import CustomUser


class InlineFavorite(admin.TabularInline):
    model = Favorite
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [InlineFavorite]

    list_display = ["id", "full_name", "email"]
    list_display_links = ["id", "full_name", "email"]

    class Meta:
        model = CustomUser
        fields = ("id", "full_name", "email", "password", "is_superuser", "is_active")
