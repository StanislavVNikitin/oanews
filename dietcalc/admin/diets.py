__all__ = ["DietAdmin"]

from django.contrib import admin
from dietcalc.models import Diet

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ("id",  "user_diet", "food", "count")