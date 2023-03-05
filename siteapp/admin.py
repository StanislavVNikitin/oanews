from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Page

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Page
        fields = '__all__'

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug', 'content', 'created_at', 'updated_at', 'is_published', 'deleted')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    fields = ('title', 'slug', 'content', 'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('views', 'created_at', 'updated_at')
    save_on_top = True
    save_as = True

admin.site.register(Page, PageAdmin)

admin.site.site_title = 'Управление страницами сайта'
admin.site.site_header = 'Управление страницами сайта'