from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from mptt.admin import DraggableMPTTAdmin

from .models import Page, MenuHome

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Page
        fields = '__all__'

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug', 'menuitem', 'content', 'created_at', 'updated_at', 'is_published', 'deleted')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    fields = ('title', 'slug', 'menuitem', 'content', 'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('views', 'created_at', 'updated_at')
    save_on_top = True
    save_as = True


admin.site.register(Page, PageAdmin)
admin.site.register(
    MenuHome,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)

admin.site.site_title = 'Управление страницами сайта'
admin.site.site_header = 'Управление страницами сайта'