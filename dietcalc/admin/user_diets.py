__all__ = ["UserDietAdmin"]

from django.contrib import admin
from dietcalc.models import UserDiet
from dietcalc.admin.admin_mixins import DeleteUndeleteMixin

@admin.register(UserDiet)
class UserDietAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    save_as = True
    save_on_top = True
    list_display = ("id", "name", "user", "is_published", "deleted")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    readonly_fields = ("id","slug", "created_at")
    fields = ("name", "gender", "age", "weight", "height", "disease", "user", "slug", "is_published", "created_at", "deleted")