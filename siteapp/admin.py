from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from .models import Page, MenuHome, UserStore


class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Page
        fields = '__all__'

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug', 'menuitem',  'created_at', 'updated_at', 'is_published', 'deleted')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    fields = ('title', 'slug', 'menuitem', 'content', 'is_published', 'views', 'created_at', 'updated_at', 'deleted')
    readonly_fields = ('views', 'created_at', 'updated_at')
    list_per_page = 20
    save_on_top = True
    save_as = True



class UserStoreAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = UserStore
        fields = '__all__'

class UserStoreAdmin(admin.ModelAdmin):
    form = UserStoreAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug', 'created_at', 'updated_at', 'is_published','is_moderated','user', 'deleted', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_moderated',)
    list_filter = ('is_moderated',)
    fields = ('title', 'slug', 'content', 'photo' , 'is_published','is_moderated','user', 'views', 'created_at', 'updated_at', 'deleted')
    readonly_fields = ('is_published','views', 'created_at', 'updated_at')
    list_per_page = 20
    save_on_top = True
    save_as = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"


admin.site.register(Page, PageAdmin)
admin.site.register(UserStore, UserStoreAdmin)
admin.site.register(
    MenuHome,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'disabled',
    ),
    list_display_links=(
        'indented_title',
    ),
)

admin.site.site_title = 'Управление страницами сайта Oanews'
admin.site.site_header = 'Управление страницами сайта Oanews'