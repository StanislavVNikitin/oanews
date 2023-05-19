__all__ = ["DiseaseAdmin"]

from django.contrib import admin
from dietcalc.models import Disease
from dietcalc.admin.admin_mixins import DeleteUndeleteMixin

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    save_as = True
    save_on_top = True
    list_display = ("id","name", "acronym", "deleted")
    list_display_links = ("name",)
    search_fields = ("name",)
    fields = ("name", "acronym", "deleted")