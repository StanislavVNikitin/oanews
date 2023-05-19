__all__ = ["DeleteUndeleteMixin"]

from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class DeleteUndeleteMixin:

    def mark_deleted(self, request, queryset):
        count = queryset.update(deleted=True)
        message = _(f"Удален, {count}")
        messages.add_message(request, messages.INFO, message)

    def un_delete(self, request, queryset):
        count = queryset.update(deleted=False)
        message = _(f"Снят с удаления, {count}")
        messages.add_message(request, messages.INFO, message)

    mark_deleted.short_description = _("Отметить на удалени")
    un_delete.short_description = _("Убрать отметку удаления")
