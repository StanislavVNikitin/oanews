from django.contrib import admin

from authapp import models


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "first_name", "last_name", "email", "is_active", "is_staff", "date_joined"]
    list_display_links = ('id', 'username', "first_name", "last_name")
    ordering = ["-date_joined"]
