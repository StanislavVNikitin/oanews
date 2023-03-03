from django.db import models
from django.urls import reverse

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название страницы")
    slug = models.SlugField(max_length=255, verbose_name="Url страницы", unique=True)
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
        return reverse("page", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["-created_at"]