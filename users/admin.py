from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email']
    list_display_links = ['id', 'full_name', 'email']

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'email', 'password', 'is_superuser', 'is_active')
