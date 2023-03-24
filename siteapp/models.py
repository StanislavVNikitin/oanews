from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

from authapp.models import CustomUser


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название страницы")
    slug = models.SlugField(max_length=255, verbose_name="Url страницы", unique=True)
    menuitem = TreeForeignKey('MenuHome', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Пункт меню')
    content = models.TextField(blank=True, verbose_name="Текст страницы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("siteapp:page_slug", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["-created_at"]



class MenuHome(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    divider = models.BooleanField(default=False, verbose_name='Разделитель')
    disabled = models.BooleanField(default=False, verbose_name='Выключение')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("siteapp:page_slug", kwargs={"slug": Page.objects.get(menuitem=self.pk).slug})
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class UserStore(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название страницы")
    slug = models.SlugField(max_length=255, verbose_name="Url страницы", unique=True)
    content = models.TextField(blank=True, verbose_name="Текст страницы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    is_moderated = models.BooleanField(default=False, verbose_name='Прошло модерацию')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userstore", verbose_name="Пользователь")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("siteapp:user_store", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Пользовательская история"
        verbose_name_plural = "Пользовательские истории"
        ordering = ["-created_at"]