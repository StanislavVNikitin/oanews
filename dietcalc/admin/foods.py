__all__ = ["FoodAdmin"]

from django.contrib import admin
from django.utils.safestring import mark_safe
from dietcalc.models import Food
from dietcalc.admin.admin_mixins import DeleteUndeleteMixin

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    save_as = True
    save_on_top = True
    list_display = ("id", "name", "category_food", "special_food", "user", "created_at", "get_photo", "deleted")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("category_food",)
    readonly_fields = ("created_at", "get_photo")
    fields = ("name","protein", "carbohydrates", "fat", "calories", "category_food", "user", "photo", "get_photo", "deleted", "created_at")

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"