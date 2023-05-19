__all__ = ["CategoryFoodAdmin"]

from django.contrib import admin
from django.utils.safestring import mark_safe
from dietcalc.models import CategoryFood
from dietcalc.admin.admin_mixins import DeleteUndeleteMixin

@admin.register(CategoryFood)
class CategoryFoodAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    save_as = True
    save_on_top = True
    list_display = ("id", "name", "get_photo", "deleted")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    readonly_fields = ("get_photo",)
    fields = ("name", "photo","get_photo", "deleted")
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"